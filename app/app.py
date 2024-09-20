from flask import Flask,request,jsonify
from functools import wraps
import ssh_server
import threading
import os
import firewall_server
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

# Dummy data for users and clients
users = {'admin': '123'}
clients = ['1']

lock = threading.Lock()

client_list = []
allowed_hosts = []


def periodic_function():
    while True:
        client_list,allowed_hosts = ssh_server.call()
        time.sleep(1)

@app.route('/submit',methods=['POST'])
def login():
    data = request.get_json()
    if (users[data['user']]==data['passw']):
        print("hi")
        return 'success'
    return 'failure'
    

@app.route('/')
def home():
    return jsonify({'client_list': client_list, 'allowed_hosts': allowed_hosts})


if __name__ == '__main__':
    threading.Thread(target=ssh_server.main).start()
    threading.Thread(target=app.run(debug=True,use_reloader=False)).start()
    threading.Thread(target=periodic_function, daemon=True).start()
    firewall_server.flush()
    