# Authors: Carnot Braun
# Email: carnotbraun@gmail.com
# Description: Script for plotting a time series of CO2 emissions from RSUs.

import pandas as pd
import matplotlib.pyplot as plt
import os

# Set the font size of the plots
plt.rcParams.update({'font.size': 20})

def load_data():
    folder_path = '/sbrc-hack/bd_rsu_csv/'
    files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    dfs = []
    
    for file in files:
        df = pd.read_csv(os.path.join(folder_path, file), sep=',',
                         names=['step', 'road_id', 'average_vehicles', 'noise_emission'])
        
        # Ensure numeric values, coercing errors to NaN
        df['step'] = pd.to_numeric(df['step'], errors='coerce')
        df['average_vehicles'] = pd.to_numeric(df['average_vehicles'], errors='coerce')
        df['noise_emission'] = pd.to_numeric(df['noise_emission'], errors='coerce')
    
        
        # Convert 'step' values from seconds to hours
        df['step'] = df['step'] / 3600  # Convert seconds to hours
        
        dfs.append(df)
    
    return pd.concat(dfs)

def plot_co2_emission_over_time(data):
    """Plot CO2 emission over time."""
    plt.figure(figsize=(9, 6))
    (data.groupby('step')['noise_emission'].mean()*5).plot(kind='line', color='b')
    plt.xlim(0, 24)
    plt.xticks(range(0, 25, 4), [f'{i}:00' for i in range(0, 25, 4)])
    plt.xlabel('Horário do Dia')
    plt.ylabel('Ruído em dB')
    plt.grid(True, linestyle=':', alpha=0.6)
    #plt.savefig(f'rsu_cologne', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function."""
    #env_id = 3  # Change to the desired environment ID
    data = load_data() #env_id)
    plot_co2_emission_over_time(data)

if __name__ == "__main__":
    main()
