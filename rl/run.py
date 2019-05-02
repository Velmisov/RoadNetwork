from rl.env import SumoEnv
from rl.gen_route import write_route_file
import traci

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import A2C

write_route_file('./nets/single-intersection-gen.rou.xml', 400000, 100000)

sumo_env = SumoEnv(net_file='./nets/single-intersection-longer.net.xml',
                   route_file='./nets/single-intersection.rou.xml',
                   out_csv_name='./outputs/a2c-contexts-5s-vmvm-400k',
                   gui=True,
                   num_seconds=400000,
                   min_green=5,
                   phases=[
                       traci.trafficlight.Phase(32000, "GGrrrrGGrrrr"),
                       traci.trafficlight.Phase(2000, "yyrrrryyrrrr"),
                       traci.trafficlight.Phase(32000, "rrGrrrrrGrrr"),
                       traci.trafficlight.Phase(2000, "rryrrrrryrrr"),
                       traci.trafficlight.Phase(32000, "rrrGGrrrrGGr"),
                       traci.trafficlight.Phase(2000, "rrryyrrrryyr"),
                       traci.trafficlight.Phase(32000, "rrrrrGrrrrrG"),
                       traci.trafficlight.Phase(2000, "rrrrryrrrrry")
                   ])

env = SubprocVecEnv([lambda: sumo_env])

# model = A2C(MlpPolicy, env, verbose=1, learning_rate=0.0001, lr_schedule='constant')
# model.learn(total_timesteps=200000)
# model.save('model')

model = A2C.load('model')
sumo_env.check(model)
