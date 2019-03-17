import sys
import traci
import subprocess
from RoadNetwork import RoadNetwork
from parse import parse

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

(nodes, edges) = parse('./name.nod.xml', 'name.edg.xml')

rn = RoadNetwork(nodes, edges)
checked = False
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    if not checked and 'veh0' in traci.vehicle.getIDList():
        checked = True
        route = rn.Deijkstra('veh0')
        print(route)
        traci.vehicle.setRoute('veh0', route)

traci.close()
sumoProcess.terminate()
