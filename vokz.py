import zmq
import json


SERVER_PUBLIC_KEY = b"R04Mg/5eW*?!hqxO=bQ)tDyCsqN@vLNfwK(Yj*sL"


class VOKZError(Exception):
    pass


def vo_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except zmq.error.ZMQError:
            raise VOKZError("Failed to connect to VO server")
    return wrapper


class Simulation(object):
    sim_type = None
    data_dir = None
    authors = None
    params = dict()    
    def from_dict(self, d):
        self.sim_type = d["sim_type"]
        self.data_dir = d["data_dir"]
        self.authors = d["authors"]
        self.params = d["params"]


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
            self.socket.connect("tcp://vo.fai.kz:5556")
        except zmq.error.ZMQError:
            raise VOKZError("Cannot connect to VO-KZ server")


    def __del__(self):
        self.socket.close()
        self.context.term()


    @vo_error
    def ping(self):
        request = {
            "type": "ping",
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())
    

    @vo_error
    def find_sim(self, sim_type: str, **kwargs):
        request = {
            "type": "find_sim",
            "data": {
                "sim_type": sim_type,
                "authors": kwargs.get("authors", None),
                "params": kwargs,
            }
        }
        self.socket.send_string(json.dumps(request))
        res = json.loads(self.socket.recv_string())
        return [ Simulation().from_dict(d) for d in res ]






