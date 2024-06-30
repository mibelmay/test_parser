import folium
import pandas as pd
from sklearn.cluster import KMeans
from folium.plugins import MarkerCluster

data = pd.DataFrame({
    'latitude': [55.1542, 55.1621, 55.1441, 55.1814, 55.1550, 55.1600, 55.1450, 55.1800],
    'longitude': [61.4282, 61.4318, 61.4033, 61.4120, 61.4290, 61.4300, 61.4050, 61.4100]
})

# кластеризация
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(data[['latitude', 'longitude']])
data['cluster'] = kmeans.labels_

# создание карты
map_center = [55.1542, 61.4282]
my_map = folium.Map(location=map_center, zoom_start=12, tiles='OpenStreetMap')

for cluster_id in data['cluster'].unique():
    marker_cluster = MarkerCluster().add_to(my_map)
    cluster_data = data[data['cluster'] == cluster_id]
    for i in range(len(cluster_data)):
        folium.Marker(
            location=[cluster_data.latitude.iloc[i], cluster_data.longitude.iloc[i]],
            popup=f"Объявление {i+1}"
        ).add_to(marker_cluster)

my_map.save('interactive_map.html')
