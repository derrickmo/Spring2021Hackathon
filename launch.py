from flask import Flask, request, url_for, jsonify
import flask
import Property
import requests
from collections import defaultdict
from Property import List
app = Flask(__name__)

@app.route('/<username>')
def get_name(username):
    return username

@app.route('/sum/<int:a>/<int:b>')
def get_sum(a,b):
    return str(a + b)


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')


def getLocation(addr):
    URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
    if addr:
        addr = addr.split(" ")
        for seg in addr:
            URL += seg
            URL += "+"
        URL = URL[:-1]
        URL += "&"

        key = "key=" + "AIzaSyAtSafk_fwKKGG2eKGIt1W_d27Any8JzrQ"
        URL += key
        PARAMS = {'address': addr}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        return (latitude, longitude)

    return [35.95, 75.16]


@app.route('/handle_data', methods=['POST'])
def handle_data():
    addr = request.form['location']
    state = request.form['state']
    city = request.form['city']
    w1 = request.form['type1']
    w2 = request.form['type2']
    w3 = request.form['type3']
    lat, lng = getLocation(addr)
    # lat, lng = [35.95, 75.16]

    houses = Property.runner(city, state, lat, lng, w1, w2, w3)
    loc_score = defaultdict(float)
    # x {id: [location, score1:price, score2:dis, score3:use]}
    for x in houses:
        lat, lng = houses[x][0]
        loc_score[str(lat) + ", "+ str(lng)] = houses[x][1]
    print(loc_score)
    return jsonify(loc_score)


    # result = {
    #     "37.782551, -122.445368":10,
    #     "37.782745, -122.444586":21,
    #     "37.782842, -122.42688":30,    
    #     "37.782919, -122.442815":33,    
    #     "37.782992, -122.442112":40,    
    #     "37.7831, -122.441461":50,    
    #     "37.783206, -122.440829":60,    
    #     "37.783273, -122.440324":75,    
    #     "37.783316, -122.440023":80,    
    #     "37.783357, -122.439794":91,    
    #     "37.783371, -122.439687":95,    
    #     "37.783368, -122.439666":99,    
    #     "37.783383, -122.439594":100,
    # }
    # return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0")