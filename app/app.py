from flask import Flask, request, jsonify
import ssh_server
import firewall_server
import threading
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

# Dummy data for users and clients
users = {'admin': '123'}
clients = ['1']

# Global variable to hold the SSH server thread
ssh_thread = None
# Flag to indicate if the SSH server is running

def periodic_function():
    while True:
        cl, ah, c = ssh_server.call()
        print(c)
        time.sleep(1)
        return cl, ah, c

@app.route('/submit', methods=['POST'])
def login():
    global ssh_thread, ssh_running  # Access global variables
    data = request.get_json()
    if (users[data['user']] == data['passw']):
        ssh_thread = threading.Thread(target=ssh_server.main)
        ssh_thread.start()  # Start the SSH server thread
        return 'success'
    return 'failure'

@app.route('/result', methods=['POST'])
def result():
    data = request.get_json()
    firewall_server.result = data
    return 'success'

@app.route('/logout', methods=['POST'])
def logout():
    global ssh_thread, ssh_running  # Access global variables
    data = request.get_json()
    if data['data'] == 'logout':
        if ssh_server.ssh_running:  
            ssh_server.ssh_running = False
            print('SSH process termination requested.')
        return 'success'
    return 'failure'

@app.route('/')
def home():
    client_list, allowed_hosts, clients = periodic_function()
    return jsonify({'client_list': client_list, 'allowed_hosts': allowed_hosts, 'clients': clients})

def run_flask_app():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    try:
        # Start a thread for periodic function
        threading.Thread(target=periodic_function).start()

        # Start the Flask app in the main thread
        run_flask_app()

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Shutting down...")
    
    finally:
        print("Shutting down the server...")
        
        firewall_server.flush()
        # Close any channels and client connections from the SSH server
        for chan in ssh_server.channels:
            chan.close()
        print('Closed the channels...')

        for client in ssh_server.client_objects:
            client.close()
        print("Closed the client connections..")

        # Ensure to clean up resources from SSH server's thread pool if applicable
        if hasattr(ssh_server, 'threadpool'):
            ssh_server.threadpool.shutdown(wait=True)  # Wait for all threads to finish
        

        if ssh_server.ssh_running:
            print('Stopping SSH server...')
            ssh_server.ssh_running = False  # Set flag to indicate that we want to stop the server

        print("Server shutdown complete.")  