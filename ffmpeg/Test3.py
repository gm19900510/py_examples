# -*- coding:utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import json

def handleReq(path):
    #url解码
    urldata = parse.unquote(path)
    
    #url结果  
    result = parse.urlparse(urldata)
    
    #url里的查询参数  
    query_dict = parse.parse_qs(result.query)
    return query_dict
   
     
class HTTPHandle(BaseHTTPRequestHandler): 

    def do_GET(self):
        if self.path != "/favicon.ico":
            print ("path:", self.path)
 
            datas = handleReq(self.path)  # 处理URL请求参数，根据参数获取相应数据
            print(datas["name"][0])  
            jsonStr = json.dumps(datas) 
            
            print (jsonStr)
            
            self.protocol_version = "HTTP/1.1"      
            self.send_response(200)       
            self.send_header("Content-type", "application/json") 
            self.end_headers()    
            self.wfile.write(str.encode(jsonStr))
             
         
def startServer():
    httpServer = HTTPServer(("192.168.3.56", 8000), HTTPHandle)
    httpServer.serve_forever()

     
if __name__ == '__main__':
    startServer()
