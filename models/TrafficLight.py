import traci


class TrafficLight:
    def __init__(self,
                 _id,
                 rn,
                 phases,
                 delta_time=5,
                 min_green=5,
                 max_green=50,
                 with_model=False):

        self.id = _id
        self.rn = rn
        self.phases = phases
        self.delta_time = delta_time
        self.min_green = min_green
        self.max_green = max_green
        self.time_on_phase = 0
        self.green_phase = 0
        self.num_green_phases = len(phases) // 2
        self.lanes = list(dict.fromkeys(traci.trafficlight.getControlledLanes(self.id)))
        self.edges = self._compute_edges()
        self.edges_capacity = self._compute_edges_capacity()
        self.yellow_time = 2

        self.controlled_lanes = traci.trafficlight.getControlledLanes(self.id)
        self.program_id = traci.trafficlight.getProgram(self.id)

        if with_model:
            logic = traci.trafficlight.Logic("new-program" + str(self.id), 0, 0, phases=phases)
            traci.trafficlight.setCompleteRedYellowGreenDefinition(self.id, logic)

    @staticmethod
    def get_ids():
        return traci.trafficlight.getIDList()

    def simulation_step(self, special_vehicle):
        if special_vehicle is None:
            if traci.trafficlight.getProgram(self.id) != self.program_id:
                traci.trafficlight.setProgram(self.id, self.program_id)
        else:
            route = special_vehicle.get_remaining_route()
            state = ''
            used_for_special_vehicle = False
            for lane in self.controlled_lanes:
                belongs = False
                for edge in route:
                    if lane.startswith(edge):
                        state += 'G'
                        belongs = True
                        used_for_special_vehicle = True
                        break
                if not belongs:
                    state += 'r'
            if used_for_special_vehicle:
                traci.trafficlight.setRedYellowGreenState(self.id, state)
            elif traci.trafficlight.getProgram(self.id) != self.program_id:
                traci.trafficlight.setProgram(self.id, self.program_id)

    @property
    def phase(self):
        return traci.trafficlight.getPhase(self.id)

    def set_next_phase(self, new_phase):
        new_phase *= 2
        if self.phase == new_phase or self.time_on_phase < self.min_green:
            self.time_on_phase += self.delta_time
            self.green_phase = self.phase
        else:
            self.time_on_phase = self.delta_time
            self.green_phase = new_phase
            traci.trafficlight.setPhase(self.id, self.phase + 1)  # turns yellow

    def update_phase(self):
        traci.trafficlight.setPhase(self.id, self.green_phase)

    def _compute_edges(self):
        return {p: self.lanes[p * 2:p * 2 + 2] for p in range(self.num_green_phases)}  # two lanes per edge

    def _compute_edges_capacity(self):
        vehicle_size_min_gap = 7.5  # 5(vehSize) + 2.5(minGap)
        return {
            p: sum([traci.lane.getLength(lane) for lane in self.edges[p]]) / vehicle_size_min_gap
            for p in range(self.num_green_phases)
        }

    def get_lanes_density(self):
        vehicle_size_min_gap = 7.5  # 5(vehSize) + 2.5(minGap)
        return [traci.lane.getLastStepVehicleNumber(lane) / (traci.lane.getLength(lane) / vehicle_size_min_gap)
                for lane in self.lanes]

    def get_lanes_queue(self):
        vehicle_size_min_gap = 7.5  # 5(vehSize) + 2.5(minGap)
        return [traci.lane.getLastStepHaltingNumber(lane) / (traci.lane.getLength(lane) / vehicle_size_min_gap)
                for lane in self.lanes]
