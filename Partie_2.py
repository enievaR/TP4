from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

messages = []
nicknames = {}

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API. Use /motd for a message of the day, /nick to set your nickname, and /msg to send or retrieve messages."})

@app.route('/motd', methods=['GET'])
def motd():
    return jsonify({"message": "Hello, World!"})

@app.route('/nick', methods=['POST'])
def set_nick():
    data = request.get_json()
    if 'nickname' not in data:
        return make_response(jsonify({"error": "Nickname is required"}), 400)
    nickname = data['nickname']
    nicknames[request.remote_addr] = nickname
    return make_response(jsonify({"message": "Nickname set"}), 201)

@app.route('/msg', methods=['POST'])
def post_msg():
    data = request.get_json()
    if 'message' not in data:
        return make_response(jsonify({"error": "Message is required"}), 400)
    messages.append(data['message'])
    return make_response(jsonify({"message": "Message added"}), 201)

@app.route('/msg', methods=['GET'])
def get_msgs():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)