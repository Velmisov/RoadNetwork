import sys
import traci
import subprocess
from models.RoadNetwork import RoadNetwork
from models.parser import parse

# added by File -> Settings -> Project interpreter -> Chosen interpreter -> add to path: /usr/share/sumo/tools
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")

port = 10080
sumoCmd = ['sumo-gui', '-c', '../data/default/default.sumocfg', '--remote-port', str(port)]

sumoProcess = subprocess.Popen(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

edges = parse('../data/default/default.net.xml')

rn = RoadNetwork(edges)
step = 0
with open('../data/theory/const_logic_direct.csv', 'w') as f:
    f.write('reward,step_time,total_stopped,total_wait_time\n')
    while not rn.empty():
        sub, waiting_time = rn.simulation_step()
        f.write('0,' + str(step) + ',0,' + str(waiting_time) + '\n')
        step += 1

traci.close()
sumoProcess.terminate()
