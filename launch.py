from datetime import timedelta

from flask import Flask, request, url_for, jsonify, globals, render_template

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


# @app.route('/<username>')
# def get_name(username):
#     return username
#
# @app.route('/sum/<int:a>/<int:b>')
# def get_sum(a,b):
#     return str(a + b)



@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """

    return render_template('index.html')

@app.route('/type', methods=['POST'])
def types():
	type1 = request.form.get('type1')
	# type2 = request.form['type2']
	# type3 = request.form['type3']
	print(type1)
	return render_template('index.html')



@app.route('/handle_data', methods=['POST'])
def handle_data():
    city = request.form['location']
    # print(city)
    result = {
	    "37.782551, -122.445368":10,
	    "37.782745, -122.444586":21,
	    "37.782842, -122.42688":30,    
	    "37.782919, -122.442815":33,    
	    "37.782992, -122.442112":40,    
	    "37.7831, -122.441461":50,    
	    "37.783206, -122.440829":60,    
	    "37.783273, -122.440324":75,    
	    "37.783316, -122.440023":80,    
	    "37.783357, -122.439794":91,    
	    "37.783371, -122.439687":95,    
	    "37.783368, -122.439666":99,    
	    "37.783383, -122.439594":100,
	}
    return jsonify(result)





if __name__ == "__main__":
    app.run(debug=True)
