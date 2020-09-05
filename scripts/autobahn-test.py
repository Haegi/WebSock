import threading
from websock.WebSocketServer import WebSocketServer


def on_data_receive(client, data):
    """
    Called by the WebSocket server when data is received.
    Echoes the received data.
    """
    server.send(client, data)


server = WebSocketServer("127.0.0.1", 9010,
                        on_data_receive=on_data_receive)
server_thread = threading.Thread(target=server.serve_forever(), args=(), daemon=True)
server_thread.start()

print('Started')
