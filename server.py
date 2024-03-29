from flask import Flask , jsonify, request , session
import requests 
import json
from flask_socketio import SocketIO


app = Flask(__name__)
app['secret_key'] = "fdjjakfjalsdfkladsfasdf"

socket = SocketIO(app  )


url = "https://api.openrouteservice.org/v2/directions/driving-car/json"
headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf624823d47e21f9b640508ab739a834ed1242',
        'Content-Type': 'application/json; charset=utf-8'
    }

@socket.on('connect' )
def init_connect():

    print("connected")
    
    socket.send("hi")
        

@app.route("/")
def home():
    return "runnning"

@socket.on('latlong')
def latlong(current_coordinates):    
    print(type(current_coordinates))
    current_coordinates = json.loads(str(current_coordinates))

    latitude = current_coordinates['latitude']
    longitude = current_coordinates['longitude']

    # print(lat , long)

    data_to_send = {
        #  "coordinates" : [[  76.94558537610791 , 8.524691394790976], [76.94545627080134 , 8.523609404305502 ]]
         "coordinates" : [[ longitude , latitude ], [76.9056140965201,8.546683266584152 ]]
    }

    recieved_data = requests.post( url , json = data_to_send, headers=headers)

   

    geojson = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', json=data_to_send, headers=headers)

    geojson = geojson.text
    recieved_data =  json.loads(recieved_data.text)
    # print(recieved_data)
    directions = recieved_data['routes'][0]['segments'][0]['steps']

    for item in directions:

        print( str(item['distance'])  +  item['instruction'])
    
    print("here")
    instructoins ={"current_distance":  f"{directions[0]['distance']}" , "current_instruction" : f"{directions[0]['instruction']}", "next_instruction" : f"{directions[1]['instruction']}", "geojson": f"{geojson}"}
    
    socket.emit('instructions', json.dumps(instructoins) ) 
    
@app.get("/get_instructions")
def give_instructions():

    # print(type(current_coordinates))
    # current_coordinates = json.loads(str(current_coordinates))

    # latitude = current_coordinates['latitude']
    # longitude = current_coordinates['longitude']

    # latitude = request.args['latitude']
    # longitude =  request.args['longitude']

    latitude = 13.01242054405569
    longitude = 80.00035241668634



    # print(lat , long)

    data_to_send = {
        #  "coordinates" : [[  76.94558537610791 , 8.524691394790976], [76.94545627080134 , 8.523609404305502 ]]
        #  "coordinates" : [[ longitude , latitude ], [76.9056140965201,8.546683266584152 ]]
         "coordinates" : [[ longitude , latitude ], [ session['lat'] ,session['long'] ]]
    }

    recieved_data = requests.post( url , json = data_to_send, headers=headers)

   

    # geojson = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', json=data_to_send, headers=headers)

    # geojson = geojson.text
    recieved_data =  json.loads(recieved_data.text)
    # print(recieved_data)
    directions = recieved_data['routes'][0]['segments'][0]['steps']

    for item in directions:

        print( str(item['distance'])  +  item['instruction'])
    
    print("here")
   
    
    return ( jsonify({'current_instruction': directions[0]['instruction'] , 'next_instruction':directions[1]['instruction'], 'distance' : directions[0]['distance']  }), 200) 

@app.route("/set_destination")
def setDestination():
    lat = request.args['lat']
    long = request.args['long']

    session['lat'] = lat
    session['long'] = long
    
    return ('', 200)
    

socket.run(app, host = "0.0.0.0", debug=True, port = 8080)
    



