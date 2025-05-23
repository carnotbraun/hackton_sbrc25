# Author: Carnot Braun
# Description: This script reads the list of edges for each RSU and converts the data from the CSV
# files to a single CSV file for each RSU.

import pandas as pd
import os
import pickle

# Folder path
folder_path = '/sbrc-hack/bd/'
#Adapt the range for all in the folder path
for rsu_id in range(13):
    # Creating a list to store the DataFrames of each CSV file
    dfs = []

    # Load the list of edges for the current RSU
    roads_file = open(f'/sbrc-hack/bd_pickle/RSU_{rsu_id}.pickle', 'rb')
    rsu_edge_list = pickle.load(roads_file)
    
    # Iterating over the CSV files and reading the data
    for file in rsu_edge_list:
        df = pd.read_csv(os.path.join(folder_path, f'{file}.csv'), sep=',')#,
                         #names=['step', 'road_id', 'road_speed', 'co2_emission',
                                #'fuel_consumption', 'average_vehicles'])

        dfs.append(df)

    # Concatenating all the DataFrames into a single DataFrame
    combined_df = pd.concat(dfs)

    # Save the combined DataFrame to CSV
    combined_df.to_csv(f'/sbrc-hack/bd_rsu_csv/RSU_{rsu_id}.csv', index=False)
