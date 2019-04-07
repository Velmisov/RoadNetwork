import traci


class TrafficLight:
    def __init__(self, _id):
        self.id = _id
        self.controlled_lanes = traci.trafficlight.getControlledLanes(self.id)
        self.program_id = traci.trafficlight.getProgram(self.id)

    @staticmethod
    def get_ids():
        return traci.trafficlight.getIDList()

    def simulation_step(self, special_vehicle):
        if special_vehicle is None:
            if traci.trafficlight.getProgram(self.id) != self.program_id:
                traci.trafficlight.setProgram(self.id, self.program_id)
        else:
            route = special_vehicle.get_route()
            state = ''
            for lane in self.controlled_lanes:
                belongs = False
                for edge in route:
                    if lane.startswith(edge):
                        state += 'G'
                        belongs = True
                        break
                if not belongs:
                    state += 'r'
            traci.trafficlight.setRedYellowGreenState(self.id, state)
