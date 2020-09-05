import threading
import unittest
import sys
import os
import time
try:
    import thread
except ImportError:
    import _thread as thread


proj_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
socket_folder = os.path.join(proj_folder, 'websocket')
sys.path.insert(0, socket_folder)

from websock import WebSocketServer

try:
    from websocket import create_connection
except ImportError:
    exit('websocket-client is required to run integrated tests: \n\n\t$ pip install websocket-client ')


class TestIntegrated(unittest.TestCase):
    """ Integrated tests on the server are run using the websocket client from
        https://github.com/websocket-client/websocket-client/blob/master/examples/echoapp_client.py
    """

    @classmethod
    def setUpClass(self):

        def on_data_receive(client, data):
            """Called by the WebSocketServer when data is received."""
            server.send(client, data)

        def on_error(exception):
            """Called when the server returns an error
            """
            raise exception

        server = WebSocketServer("127.0.0.1", 8467, on_data_receive=on_data_receive, on_error=on_error)
        server_thread = threading.Thread(target=server.serve_forever, args=(), daemon=True)
        server_thread.start()

    def test_echo_server_single_client(self):
        ws = create_connection("ws://localhost:8467")
        ws.send("Hello, World")
        result = ws.recv()
        ws.close()

        self.assertEqual(result, "Hello, World")

    def test_echo_server_65535_message(self):
        ws = create_connection("ws://localhost:8467")
        payload = "*" * 65535
        ws.send(payload)
        result = ws.recv()
        time.sleep(1)
        ws.close()

        self.assertEqual(len(result), len(payload))
        self.assertEqual(result, payload)

    def test_echo_server_65536_message(self):
        ws = create_connection("ws://localhost:8467")
        payload = "*" * 65536
        ws.send(payload)
        result = ws.recv()
        time.sleep(1)
        ws.close()

        self.assertEqual(len(result), len(payload))
        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main()
