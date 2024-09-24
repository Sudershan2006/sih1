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

# client_list = []
# allowed_hosts = []



def periodic_function():
    # global client_list,allowed_hosts
    while True:
        cl,ah,c = ssh_server.call()
        # client_list=cl
        # allowed_hosts=ah
        time.sleep(1)
        return cl,ah,c

@app.route('/submit',methods=['POST'])
def login():
    data = request.get_json()
    if (users[data['user']]==data['passw']):
        return 'success'
    return 'failure'

@app.route('/result',methods=['POST'])
def result():
    data = request.get_json()
    firewall_server.result = data
    print('hi')
    return 'success'
    

@app.route('/')
def home():
    client_list,allowed_hosts,clients = periodic_function()
    return jsonify({'client_list': client_list, 'allowed_hosts': allowed_hosts,'clients': clients})


if __name__ == '__main__':
    threading.Thread(target=periodic_function, daemon=True).start()
    threading.Thread(target=ssh_server.main).start()
    threading.Thread(target=app.run(debug=True,use_reloader=False)).start()
    firewall_server.flush()
    