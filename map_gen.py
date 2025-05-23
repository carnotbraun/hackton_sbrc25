# Author: Carnot Braun
# Description: Script for generating a map of average noise emissions from a traffic simulation scenario (LuST).
import pandas as pd
import os
import xml.etree.ElementTree as ET
from shapely.geometry import LineString
import geopandas as gpd
import matplotlib.pyplot as plt

# Calcular média de emissão por edge (com base em vários arquivos .csv)
folder_path = "/sbrc-hack/bd/"
noise_data = []

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        road_id = filename.replace(".csv", "")
        df = pd.read_csv(os.path.join(folder_path, filename), sep=",")
        avg_noise = df["noise_emission"].mean()
        noise_data.append({"road_id": road_id, "avg_noise_emission": avg_noise})

df_noise = pd.DataFrame(noise_data)

# Parsear o .net.xml e extrair geometria das ruas
tree = ET.parse("/LuSTScenario/scenario/lust.net.xml")
root = tree.getroot()

geometries = []

for edge in root.findall("edge"):
    edge_id = edge.get("id")
    if edge_id.startswith(":"):
        continue  # Ignorar edges internos

    for lane in edge.findall("lane"):
        shape_str = lane.get("shape")
        if not shape_str:
            continue
        points = [(float(x), float(y)) for x, y in (p.split(",") for p in shape_str.split())]
        geometry = LineString(points)
        geometries.append({"road_id": edge_id, "geometry": geometry})

gdf_edges = gpd.GeoDataFrame(geometries, crs="EPSG:32632")  # UTM 32N (aproximadamente o usado no LuST)

# Juntar dados de ruído com geometria
gdf_merged = gdf_edges.merge(df_noise, on="road_id", how="left")
gdf_merged = gdf_merged[gdf_merged["avg_noise_emission"].notna()]  # Remove edges sem dados

# Plotar o mapa 
fig, ax = plt.subplots(figsize=(10, 8))
gdf_merged.plot(column="avg_noise_emission", cmap="inferno", linewidth=1, legend=True, ax=ax)
plt.title("Mapa de Emissão Média de Ruído por Rua (LuST)", fontsize=16)
plt.axis("off")
plt.savefig("mapa_ruido_lust.png", dpi=300, bbox_inches="tight")
#plt.show()

import seaborn as sns

#  Extrair coordenadas do centro de cada rua (LineString)
gdf_merged["x"] = gdf_merged.geometry.centroid.x
gdf_merged["y"] = gdf_merged.geometry.centroid.y

#  Criar o jointplot hexbin com seaborn
sns.set(style="white", font_scale=1.2)
plot = sns.jointplot(
    data=gdf_merged,
    x="x",
    y="y",
    kind="hex",
    gridsize=22,
    cmap="inferno",
    marginal_kws=dict(bins=50, fill=True),
)

plot.fig.suptitle("Densidade de Emissão de Ruído no Cenário LuST", y=1.02)
plot.set_axis_labels("X (metros)", "Y (metros)")

# Salvar figura
plot.fig.savefig("heatmap_hexbin_ruido.png", dpi=300,bbox_inches="tight")
