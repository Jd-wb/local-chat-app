import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import subprocess  # To run scripts or commands

# File to store chat rooms and their messages
CHAT_ROOMS_FILE = "chat_rooms.json"

# Load chat rooms from file, or return an empty dictionary if the file doesn't exist
def load_chat_rooms():
    if os.path.exists(CHAT_ROOMS_FILE):
        with open(CHAT_ROOMS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save chat rooms and their messages to a file
def save_chat_rooms(chat_rooms):
    with open(CHAT_ROOMS_FILE, "w") as f:
        json.dump(chat_rooms, f)

# Custom request handler to handle chat-related actions
class ChatHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        query_params = parse_qs(self.path[2:])  # Strip the leading '/'
        
        if self.path.startswith("/join_chat"):
            code = query_params.get('code', [''])[0]
            chat_rooms = load_chat_rooms()
            if code in chat_rooms:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Chat not found!"}).encode())

        elif self.path.startswith("/create_chat"):
            code = query_params.get('code', [''])[0]
            chat_rooms = load_chat_rooms()
            if code in chat_rooms:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Chat already exists!"}).encode())
            else:
                chat_rooms[code] = []
                save_chat_rooms(chat_rooms)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
        
        elif self.path.startswith("/get_messages"):
            code = query_params.get('code', [''])[0]
            chat_rooms = load_chat_rooms()
            if code in chat_rooms:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"messages": chat_rooms[code]}).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"messages": []}).encode())

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/send_message":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode()
            post_params = parse_qs(post_data)
            message = post_params.get('message', [''])[0]
            code = post_params.get('code', [''])[0]
            
            chat_rooms = load_chat_rooms()
            if code in chat_rooms:
                chat_rooms[code].append(message)
                save_chat_rooms(chat_rooms)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Message received")
            else:
                self.send_response(404)
                self.end_headers()

    # New POST request to start the server when the spacebar is pressed
    def do_POST_start_server(self):
        if self.path == "/start-server":
            try:
                # You could call subprocess to run your app.py
                # Alternatively, you can adjust this to match what you need to trigger
                subprocess.Popen(['python3', 'app.py'])  # Start the app.py script
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Server started!"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())

def run_server():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, ChatHTTPRequestHandler)
    print("Server running at http://localhost:8000/")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
