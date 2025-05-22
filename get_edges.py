# Author: Carnot Braun & Allan M. de Souza
# Email: carnotbraun@gmail.com & allanms@unicamp.br
# Description: Script for extracting road data from SUMO simulation.

import os
import sys
import csv

# Add dict to use as label for the environment > 1 = lust, 2 = most, 3 = cologne
env = {1: 'lust', 2: 'most', 3: 'cologne'}
# Add SUMO tools directory to the system path
sys.path.append(os.path.join('c:', os.sep, '/Users/carnotbraun/mestrado/simu/sumo/tools'))

# Now you can import traci
import traci
import sumolib

# Function to execute the SUMO simulation
def run_simulation(config_file):
    sumo_exec = "/Users/carnotbraun/mestrado/simu/sumo/bin/sumo"
    sumo_cmd = [sumo_exec, "-c", config_file, "--tripinfo-output", 
                'output.xml', "--scale", '0.3','--threads', '8']
    
    try:
        traci.start(sumo_cmd)
        step = 0
        edges_list = traci.edge.getIDList()
        
        while traci.simulation.getMinExpectedNumber() > 0:
            if step % 60 == 0:
                print(f'Writing Traffic dataset step {step} ...')
                for edge in edges_list:
                    if edge.startswith(':'):
                        continue
                    average_vehicles = traci.edge.getLastStepVehicleNumber(edge)
                    noise_emission = traci.edge.getNoiseEmission(edge)
                    
                    filepath = f'/Users/carnotbraun/sbrc-hack/bd/{edge}.csv'
                    
                    with open(filepath, 'a') as road_file:
                        writer = csv.writer(road_file)
                        if os.stat(road_file.name).st_size == 0:  # Check if file is empty
                            writer.writerow(['step', 'road_id', 'average_vehicles', 'noise_emission'])
                        writer.writerow([step, edge, average_vehicles, noise_emission])
                
            traci.simulationStep()
            step += 1
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        traci.close()
        print("SUMO simulation completed")

# Main function
def main():
    config_file = "/Users/carnotbraun/mestrado/simu/LuSTScenario/scenario/due.actuated.sumocfg"
    run_simulation(config_file)

# Execute main function
if __name__ == "__main__":
    main()
