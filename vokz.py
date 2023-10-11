import zmq
import json

SERVER_PUBLIC_KEY = b"82M+$O0^qkJRj8/nWi[cma-4916*miCcALuf2-&e"


class voError(Exception):
    pass


def vo_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except zmq.error.ZMQError:
            raise ConnectionError("Failed to connect to VO server")
    return wrapper


class Client(object):
    def __init__(self, api_key):
        self.client_public_key = api_key[:40].encode('ascii')
        self.client_secret_key = api_key[40:].encode('ascii')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.curve_secretkey = self.client_secret_key
        self.socket.curve_publickey = self.client_public_key
        self.socket.curve_serverkey = SERVER_PUBLIC_KEY
        try:
            self.socket.connect("tcp://vo.fai.kz:5555")
        except zmq.error.ZMQError:
            raise ConnectionError("Cannot connect to VO server")

    def __del__(self):
        self.socket.close()
        self.context.term()

    @vo_error
    def get_submissions(self):
        request = {
            "type": "submissions",
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())
    






