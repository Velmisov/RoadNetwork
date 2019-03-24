import sys
import traci
import subprocess
from RoadNetwork import RoadNetwork
from parse import parse
from Vehicle import Vehicle

# added by File -> Settings -> Project interpreter -> Chosen interpreter -> add to path: /usr/share/sumo/tools
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")

port = 10080
sumoCmd = ['sumo-gui', '-c', 'name.sumocfg', '--remote-port', str(port)]

sumoProcess = subprocess.Popen(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

edges = parse('./name.net.xml')

rn = RoadNetwork(edges)
vehicles = {}
while not rn.empty():
    rn.simulation_step()
    active_vehicles = traci.vehicle.getIDList()
    for vehicle_id in active_vehicles:
        if vehicle_id not in vehicles:
            vehicles[vehicle_id] = Vehicle(vehicle_id)
            route = rn.Deijkstra(vehicle_id)
            print(route)
            traci.vehicle.setRoute(vehicle_id, route)

traci.close()
sumoProcess.terminate()
