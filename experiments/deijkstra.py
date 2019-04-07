import sys
import traci
import subprocess
from models.RoadNetwork import RoadNetwork
from models.parser import parse
from models.Vehicle import Vehicle

# added by File -> Settings -> Project interpreter -> Chosen interpreter -> add to path: /usr/share/sumo/tools
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")

port = 10080
sumoCmd = ['sumo-gui', '-c', '../data/deijkstra/deijkstra.sumocfg', '--remote-port', str(port)]

sumoProcess = subprocess.Popen(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

edges = parse('../data/deijkstra/deijkstra.net.xml')

rn = RoadNetwork(edges)
vehicles = {}
while not rn.empty():
    rn.simulation_step()
    active_vehicles = traci.vehicle.getIDList()
    for vehicle_id in active_vehicles:
        if vehicle_id not in vehicles:
            vehicles[vehicle_id] = Vehicle(vehicle_id)
            route = rn.Deijkstra(vehicle_id, rn.mean_speed_weight)
            print(route)
            traci.vehicle.setRoute(vehicle_id, route)

traci.close()
sumoProcess.terminate()
