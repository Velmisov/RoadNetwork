import traci


class TrafficLight:
    def __init__(self, _id):
        self.id = _id

    @staticmethod
    def get_ids():
        return traci.trafficlight.getIDList()

    def simulation_step(self):
        pass
