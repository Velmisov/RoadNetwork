import sumolib
import traci
import numpy as np
import pandas as pd
import gym
from gym import spaces

from .trafficsignal import TrafficSignal


class SumoEnv(gym.Env):
    def __init__(self,
                 net_file,
                 route_file,
                 phases,
                 out_csv_name=None,
                 gui=False,
                 num_seconds=20000,
                 time_to_load_vehicles=120,
                 delta_time=5,
                 min_green=5,
                 max_green=50):

        self._net = net_file
        self._route = route_file
        self._gui = gui
        if self._gui:
            self._sumo_binary = sumolib.checkBinary('sumo-gui')
        else:
            self._sumo_binary = sumolib.checkBinary('sumo')

        traci.start([sumolib.checkBinary('sumo'), '-n', self._net])

        self.ts_id = traci.trafficlight.getIDList()[0]
        self.lanes_per_ts = len(set(traci.trafficlight.getControlledLanes(self.ts_id)))
        self.traffic_signal = None
        self.phases = phases
        self.num_green_phases = len(phases) // 2
        self.vehicles = dict()
        self.last_measure = 0  # used to reward function remember last measure
        self.last_reward = 0
        self.sim_max_time = num_seconds
        self.time_to_load_vehicles = time_to_load_vehicles
        self.delta_time = delta_time  # seconds on sumo at each step
        self.min_green = min_green
        self.max_green = max_green
        self.yellow_time = 2

        """
        Default observation space is a vector R^(#greenPhases + 1 + 2 * #lanes)
        s = [current phase one-hot encoded, elapsedTime / maxGreenTime, density for each lane, queue for each lane]
        Action space is which green phase is going to be open for the next delta_time seconds
        """
        self.observation_space = spaces.Box(low=np.zeros(self.num_green_phases + 1 + 2 * self.lanes_per_ts),
                                            high=np.ones(self.num_green_phases + 1 + 2 * self.lanes_per_ts))
        self.discrete_observation_space = spaces.Tuple((
            spaces.Discrete(self.num_green_phases),  # Green Phase
            spaces.Discrete(self.max_green // self.delta_time),  # Elapsed time of phase
            *(spaces.Discrete(10) for _ in range(2 * self.lanes_per_ts))  # Density and stopped-density for each lane
        ))
        self.action_space = spaces.Discrete(self.num_green_phases)

        self.run = 0
        self.metrics = []
        self.out_csv_name = out_csv_name

        traci.close()

    def reset(self):
        if self.run != 0:
            self.save_csv(self.out_csv_name, self.run)
        self.run += 1
        self.metrics = []

        sumo_cmd = [self._sumo_binary,
                    '-n', self._net,
                    '-r', self._route,
                    '--max-depart-delay', '0',
                    '--waiting-time-memory', '10000',
                    '--random']
        if self._gui:
            sumo_cmd.append('--start')
        traci.start(sumo_cmd)

        self.traffic_signal = TrafficSignal(self,
                                            self.ts_id,
                                            self.delta_time,
                                            self.min_green,
                                            self.max_green,
                                            self.phases)
        self.last_measure = 0

        self.vehicles = dict()

        # for _ in range(self.time_to_load_vehicles):
        #     traci.simulationStep()

        return self._compute_observations()

    @property
    def sim_step(self):
        return traci.simulation.getCurrentTime() / 1000  # milliseconds to seconds

    def step(self, action):
        self._apply_action(action)

        # run simulation for delta time
        for _ in range(self.yellow_time):
            traci.simulationStep()
        self.traffic_signal.update_phase()
        for _ in range(self.delta_time - self.yellow_time):
            traci.simulationStep()

        # observe new state and reward
        observation = self._compute_observations()
        reward = self._compute_rewards()
        done = self.sim_step > self.sim_max_time
        info = self._compute_step_info()
        self.metrics.append(info)
        self.last_reward = reward

        return observation, reward, done, {}

    def check(self, model):
        self.reset()
        step = 0
        with open(self.out_csv_name, 'w') as f:
            f.write('reward,step_time,total_stopped,total_wait_time\n')
            while traci.simulation.getMinExpectedNumber() > 0:
                observation = self._compute_observations()
                action = model.predict(observation)[0]
                self._apply_action(action)
                # run simulation for delta time
                for _ in range(self.yellow_time):
                    traci.simulationStep()
                self.traffic_signal.update_phase()
                for _ in range(self.delta_time - self.yellow_time):
                    traci.simulationStep()
                waiting_time = self.traffic_signal.get_waiting_time()
                f.write('0,' + str(step) + ',0,' + str(waiting_time) + '\n')
                step += 1

    def _apply_action(self, action):
        """
        Set the next green phase for the traffic signals
        :param action: action is an int between 0 and self.num_green_phases (next green phase)
        """
        self.traffic_signal.set_next_phase(action)

    def _compute_observations(self):
        phase_id = [1 if self.traffic_signal.phase // 2 == i else 0 for i in
                    range(self.num_green_phases)]  # one-hot encoding
        elapsed = self.traffic_signal.time_on_phase / self.max_green
        density = self.traffic_signal.get_lanes_density()
        queue = self.traffic_signal.get_lanes_queue()
        return phase_id + [elapsed] + density + queue

    def _compute_rewards(self):
        return self._waiting_time_reward()

    def _waiting_time_reward(self):
        ts_wait = self.traffic_signal.get_waiting_time()
        rewards = self.last_measure - ts_wait
        self.last_measure = ts_wait
        return rewards

    def _compute_step_info(self):
        return {
            'step_time': self.sim_step,
            'reward': self.last_reward,
            'total_stopped': sum(self.traffic_signal.get_stopped_vehicles_num()),
            'total_wait_time': self.last_measure
        }

    def close(self):
        traci.close()

    def save_csv(self, out_csv_name, run):
        if out_csv_name is not None:
            df = pd.DataFrame(self.metrics)
            df.to_csv(out_csv_name + '_run{}'.format(run) + '.csv', index=False)
