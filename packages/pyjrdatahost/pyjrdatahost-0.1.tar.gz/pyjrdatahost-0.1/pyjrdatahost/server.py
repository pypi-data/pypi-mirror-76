""" Example of json-rpc usage with Wergzeug and requests.
NOTE: there are no Werkzeug and requests in dependencies of json-rpc.
NOTE: server handles all url paths the same way (there are no different urls).
"""

# 依赖：werkzeug,requests
# 对于100MB以下数据的存储速度较快。32M大小的文件，访问时间大约0.43s。
# 支持pypy，但是速度提升不明显。
# 可以传输：np.ndarray,pd.DataFrame等数组。
# 原理：
#get_data:将base64数据嵌入到json中发送给客户端，客户端用base64解码之后，再通过pickle还原对象。
#set_data: 在客户端将数据pickle为二进制对象之后，进行base64化，然后嵌入到json中发送到服务端。
#                服务端直接存储base64的数据。
#编码解码过程都发生在客户端。
# 使用包：pip install json-rpc,python3以上可用。

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher
import time


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]

class Server():
    def __init__(self):
        self.data_dic={}# 存储的是data的base64值。
           
    def set_data(self,name:str,data_b64):
        '''如果没有数据，就添加数据。
        如果有数据，就替换数据。
        '''
        self.data_dic[name]=data_b64
        print(self.data_dic.keys())
        return "set data ok!"

    def get_data(self,name:str):
        return self.data_dic[name]
    
    @Request.application
    def application(self,request):
        # Dispatcher is dictionary {<method_name>: callable}
        t0=time.time()
        global data
        dispatcher["add"] = lambda a, b: encoded_data
        dispatcher['set_data'] = lambda name,data: self.set_data(data_b64=data,name=name)
        dispatcher['get_data'] = lambda name:self.get_data(name=name)
        
        response = JSONRPCResponseManager.handle(
            request.get_data(cache=False, as_text=True), dispatcher)
        r = Response(response.json, mimetype='application/json')
        t1=time.time()
        print(t1-t0)
        return r
    
    



if __name__ == '__main__':
    s=Server()
    run_simple('localhost', 4000, s.application)
    