import sys
import traci
import subprocess
from models.RoadNetwork import RoadNetwork
from models.parser import parse
from stable_baselines import A2C

# added by File -> Settings -> Project interpreter -> Chosen interpreter -> add to path: /usr/share/sumo/tools
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")

port = 10080
sumoCmd = ['sumo-gui', '-c', './data/2tls_rl/2tls.sumocfg', '--remote-port', str(port)]

sumoProcess = subprocess.Popen(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

edges = parse('./data/2tls_rl/2tls.net.xml')

model = A2C.load('./rl/model')

rn = RoadNetwork(edges, None, model, [traci.trafficlight.Phase(32000, "GGrrrrGGrrrr"),
                                      traci.trafficlight.Phase(2000, "yyrrrryyrrrr"),
                                      traci.trafficlight.Phase(32000, "rrGrrrrrGrrr"),
                                      traci.trafficlight.Phase(2000, "rryrrrrryrrr"),
                                      traci.trafficlight.Phase(32000, "rrrGGrrrrGGr"),
                                      traci.trafficlight.Phase(2000, "rrryyrrrryyr"),
                                      traci.trafficlight.Phase(32000, "rrrrrGrrrrrG"),
                                      traci.trafficlight.Phase(2000, "rrrrryrrrrry")])

rn.run_with_model()

# while not rn.empty():
#     traci.simulationStep()

traci.close()
sumoProcess.terminate()
