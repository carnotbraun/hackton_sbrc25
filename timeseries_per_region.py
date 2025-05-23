# Author: Carnot Braun
# Description: Script for generating a map of average noise emissions from a traffic simulation scenario (LuST).
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Diretórios dos dados
base_dir = "/sbrc-hack"
csv_dir = os.path.join(base_dir, "bd")
pickle_dir = os.path.join(base_dir, "bd_pickle")

# Agregador geral
rsu_noise_data = {}

# Iterar sobre os arquivos pickle de RSU
for pickle_file in os.listdir(pickle_dir):
    if pickle_file.endswith(".pickle"):
        rsu_id = pickle_file.replace("RSU_", "").replace(".pickle", "")
        
        # Carrega edges cobertas por esta RSU
        with open(os.path.join(pickle_dir, pickle_file), "rb") as f:
            covered_edges = pickle.load(f)
        
        # Inicializa lista de dados
        rsu_noise_data[rsu_id] = []

        # Itera sobre as edges e junta os dados de ruído
        for edge in covered_edges:
            edge_file = os.path.join(csv_dir, f"{edge}.csv")
            if os.path.exists(edge_file):
                df = pd.read_csv(edge_file)
                df['rsu_id'] = rsu_id
                df['noise_emission'] *= 5  # <--- aqui multiplicamos por 10
                rsu_noise_data[rsu_id].append(df[['step', 'noise_emission', 'rsu_id']])


# Junta tudo em um único DataFrame
df_all = pd.concat([pd.concat(dfs) for dfs in rsu_noise_data.values()])

#sns.histplot(data = df_all, x = 'noise_emission', bins = 100, kde = True)
# Agrupa por tempo e RSU, calcula ruído médio
df_grouped = df_all.groupby(['step', 'rsu_id'])['noise_emission'].mean().reset_index()

# 📈 Plot: linha do tempo do ruído médio por RSU
plt.figure(figsize=(14, 8))
sns.set(style="whitegrid", font_scale=1.2)
palette = sns.color_palette("tab20", n_colors=df_grouped['rsu_id'].nunique())

# Linha do tempo do ruído médio por RSU
sns.lineplot(
    data=df_grouped,
    x='step',
    y='noise_emission',
    hue='rsu_id',
    palette=palette,
    linewidth=2
)

plt.title("Evolução do Ruído Médio por Região (RSU) ao Longo do Tempo", fontsize=18, weight='bold')
plt.xlabel("Tempo (Step)", fontsize=14)
plt.ylabel("Ruído Médio (dB)", fontsize=14)
plt.legend(
    title="ID da RSU",
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    borderaxespad=0,
    frameon=True,
    fontsize=12,
    title_fontsize=13
)
plt.tight_layout(pad=2)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.subplots_adjust(right=0.8)
plt.show()
