import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def get_message():
    print(os.environ.get('MESSAGE'))
    message = os.environ.get('MESSAGE', 'Hello World defautlt !!')
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(port=os.environ.get('APP_PORT', 5555))
