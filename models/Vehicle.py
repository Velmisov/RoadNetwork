import traci


class Vehicle:
    def __init__(self, _id):
        self.id = _id

    def __str__(self):
        return "Vehicle. id:'" + self.id + "'"

    def get_accel(self):
        return traci.vehicle.getAccel(self.id)

    def get_decel(self):
        return traci.vehicle.getDecel(self.id)

    def get_max_speed(self):
        return traci.vehicle.getMaxSpeed(self.id)

    def get_first_edge(self):
        if self.id not in traci.vehicle.getIDList():
            return None
        route = traci.vehicle.getRoute(self.id)
        if len(route) == 0:
            return None
        return route[0]

    def get_last_edge(self):
        if self.id not in traci.vehicle.getIDList():
            return None
        route = traci.vehicle.getRoute(self.id)
        if len(route) == 0:
            return None
        return route[-1]

    def get_route(self):
        return traci.vehicle.getRoute(self.id)

    def get_remaining_route(self):
        all_route = self.get_route()
        return all_route[traci.vehicle.getRouteIndex(self.id):]
