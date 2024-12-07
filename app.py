from flask import Flask, session, request, jsonify
from flask_session import Session
import os
import redis
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)



Session(app)


@app.route('/start', methods=['GET'])
def start_session():
    session['user_id'] = session.sid
    session['history'] = []

    return jsonify({"message": "Session started!",
                     "session_id": session['user_id']
                     }), 200


def bot_respond(user_message):
    bot_response = f"user said, {user_message}"
    return bot_response

@app.route('/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message')
    if 'user_id' not in session:
        return jsonify({"error": "No active session"}), 400
    
    session['history'].append({"user": user_message})
    bot_reply = bot_respond(user_message)
    session['history'].append({'bot': bot_reply})

    return jsonify({"reply": bot_reply,
                    "history": session['history']
                    }), 200

@app.route('/end', methods=['GET'])
def end_session():
    session.clear()
    return jsonify(message="Session ended!"), 200

if __name__ == '__main__':
    app.run(debug=True)