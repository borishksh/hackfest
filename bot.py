from flask import Flask, jsonify, request
from flask_cors import CORS
from hugchat import hugchat
from hugchat.login import Login
import os

app = Flask(__name__)
CORS(app)

# Define a directory to store cookies
cookie_path_dir = "./cookies_snapshot"
chatbot = None

# Function to initialize hugchat and log in
def initialize_hugchat(email, password):
    global chatbot
    if chatbot is None:
        sign = Login(email, password)
        cookies = sign.login()
        sign.saveCookiesToDir(cookie_path_dir)
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

@app.route('/login', methods=['POST'])
def user_login():
    data = request.json  # Assuming you're sending JSON data
    email = data.get('email')
    password = data.get('password')
    message = data.get('message')

    # Check email and password (replace with your authentication logic)
    if email == 'nightfeury129@gmail.com' and password == 'Borish123@':
        # Initialize hugchat and log in if not already logged in
        initialize_hugchat(email, password)
        
        # Chat with the bot and get the response
        chat = chatbot.chat(message)
        
        return jsonify({'message': chat})
    else:
        return jsonify({'message': 'Login failed'})

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json  # Assuming you're sending JSON data
    message = data.get('message')
    
    # Check if the chatbot is initialized
    if chatbot is not None:
        # Chat with the bot and get the response
        chat = chatbot.chat(message)
        return jsonify({'message': chat})
    else:
        return jsonify({'message': 'Chatbot not initialized'})

if __name__ == '__main__':
    app.run(debug=True)