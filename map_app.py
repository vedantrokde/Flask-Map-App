# importing foliumn library
import folium
import pandas as pd

# reading volcano co-ordinates
volcano = pd.read_csv("volcanos.csv")
lat = volcano["LAT"].to_list()
lon = volcano["LON"].to_list()
elev = volcano["ELEV"].to_list()

# reading GeoJson of world population
population = open("world.json", "r", encoding="utf-8-sig").read()

# util functions
def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


# creating map
map = folium.Map(location=[38, -99], zoom_start=6)


# creating volcano feature group
volcano_group = folium.FeatureGroup(name="Volcano")

# adding markers for volcanos
for lt, ln, el in zip(lat, lon, elev):
    volcano_group.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            radius=6,
            popup=str(el) + " m",
            fill_color=color_producer(el),
            fill=True,
            color="grey",
            fill_opacity=0.7,
        )
    )


# creating population feature group
population_group = folium.FeatureGroup(name="Population")

# adding area map for population
population_group.add_child(
    folium.GeoJson(
        data=population,
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10000000
            else "pink"
            if 10000000 <= x["properties"]["POP2005"] < 20000000
            else "purple"
            if 20000000 <= x["properties"]["POP2005"] < 50000000
            else "orange"
            if 50000000 <= x["properties"]["POP2005"] < 100000000
            else "red"
        },
        zoom_on_click=True
    )
)


# adding feature groups to the map
map.add_child(population_group)
map.add_child(volcano_group)
map.add_child(folium.LayerControl())

map.save("index.html")
