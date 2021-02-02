from flask import Flask, request, jsonify
from pewdiepython import User

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/analyze', methods=['GET'])
def analyze():
    if 'username' in request.args:
        username = str(request.args['username'])
        user = User(username)
        colors = user.analyze()
        return jsonify(colors)
    else:
        return "Error"
