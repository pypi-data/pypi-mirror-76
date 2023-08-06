import requests
import json
import base64
import pickle
import time
import sys
import numpy as np

class Client():
    def __init__(self):
        pass
    def set_data(self,name:str,data:object):
        t0=time.time()
        url = "http://localhost:4000/jsonrpc"
        data_b64=base64.b64encode(pickle.dumps(data)).decode('ascii')
        # Example echo method
        
        payload = {
            "method": "set_data",
            "params": [name,data_b64],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url, json=payload).json()
        t1=time.time()
        print(response)
        print('set value,time elapsed',t1-t0,'size is %f MB'%(sys.getsizeof(data_b64)*1.0/(1024*1024*1.0)),'\n\n')

    def get_data(self,name:str):
        t0=time.time()
        url = "http://localhost:4000/jsonrpc"

        # Example echo method
        payload = {
            "method": "get_data",
            "params": [name],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url, json=payload).json()
        t1=time.time()
        resp_bytes = response['result'].encode('ascii')
        pkl_bytes = base64.b64decode(resp_bytes)
        data = pickle.loads(pkl_bytes)
        t2 = time.time()
        hash(response['result'])
        t3 = time.time()
        print('get value,time elapsed:\n','request:',t1-t0,'total:',t2-t0,'\ndecoding:',t2-t1,'hashing:',t3-t2)
        print(data,'\n','size is %f MB'%(sys.getsizeof(response['result'])*1.0/(1024*1024*1.0)))
        print('')
        return data



if __name__ == "__main__":
    c=Client()
    c.set_data('a','hhhhhhhhhhhhhhhhhh')
    c.get_data('a')
    c.set_data('b',np.empty(shape=(1024*2,1024*2,3),dtype=np.uint16))# 模拟，传输一张较大的图片。
    print(c.get_data('b'))