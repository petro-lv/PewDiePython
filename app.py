from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pewdiepython import User, User_logged, ResultEncoder

app = Flask(__name__)
app.config['DEBUG'] = True
app.json_encoder = ResultEncoder

cors = CORS(app)

instagramUsername = 'username'
instagramUsernameHeader = 'Insta-Username'
instagramPasswordHeader = 'Insta-Password'


@app.route('/api/instagram/analyze', methods=['GET'])
@cross_origin()
def analyze():
    if instagramUsername in request.args:
        username = str(request.args[instagramUsername])

        user = User(username)
        colors = user.analyze()

        return jsonify(colors)
    else:
        return "Error", 400


@app.route('/api/instagram/analyze-top', methods=['GET'])
@cross_origin()
def analyze_following():
    if instagramUsernameHeader and instagramPasswordHeader in request.headers:
        username = str(request.headers.get(instagramUsernameHeader))
        password = str(request.headers.get(instagramPasswordHeader))

        user = User_logged(username, password)
        colors = user.analyze_top()

        return jsonify(colors)
    else:
        return "Error", 400
