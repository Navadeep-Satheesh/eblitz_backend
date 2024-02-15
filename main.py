import openrouteservice as ors 
import folium 

client = ors.Client(key = "5b3ce3597851110001cf624823d47e21f9b640508ab739a834ed1242")

# coordinates = [[8.524200, 76.942890], [8.488630, 76.951940]]
coordinates = [[ 76.94552817193767 , 8.524396406995063], [76.94545627080134 , 8.523609404305502 ]]

route = client.directions(coordinates = coordinates , profile = "driving-car", format = "geojson")


directions = route['features'][0]['properties']['segments'][0]['steps']

# print(directions)

for item in directions:
    print(item.get("distance") , item.get("instruction"), item.get("name"))


