import json
from flask import Flask, render_template, jsonify, request, send_from_directory
import os
from chatbot import predict_class, get_response

app = Flask(__name__, static_folder='static')

# Load the intents file and initialize the chatbot
intents_path = r'C:\Users\admin\Desktop\chatbot\chatbot\Include\intents.json'
intents = json.loads(open(intents_path).read())

# Serve static files, including images
@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# Home route
@app.route('/')
def home():
    return render_template('chatbot.html')
 
# Route to get chatbot response
@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.form['user_message']
    intents_list = predict_class(user_message)
    chatbot_response = get_response(intents_list, intents)

    if isinstance(chatbot_response, list) and chatbot_response:
        # If the chatbot response is a list, extract the first response
        response_text = chatbot_response[0]['response']
    else:
        # If the chatbot response is a string or empty, use it as is
        response_text = chatbot_response

    return jsonify({'bot_response': response_text})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
