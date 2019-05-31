# -*- coding:utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import redis
from tools.http_tool import handle
  
class HTTPTool(BaseHTTPRequestHandler): 
        
    def do_GET(self):
        
        return_data = handle(r, args, self.path) 
        self.protocol_version = "HTTP/1.1"      
        self.send_response(200)       
        self.send_header("Content-type", "application/json") 
        self.end_headers()    
        self.wfile.write(str.encode(return_data)) 

      
def startServer():
    
    httpServer = HTTPServer(("192.168.3.56", 8000), HTTPTool)
    httpServer.serve_forever()
    
     
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='controller')
    parser.add_argument("-ffmpeg_path", "--ffmpeg_path", default='C:/Users/Administrator/Desktop/EasyNVR-windows-3.0.0-1810081104/ffmpeg.exe', help='path to ffmpeg.')
    parser.add_argument("-rtmp_path", "--rtmp_path", default='rtmp://192.168.3.56:1935/live/', help='path to rtmp.')
    parser.add_argument('-mqtt_host', '--mqtt_host', default='192.168.3.202', help='')
    parser.add_argument('-mqtt_port', '--mqtt_port', default=1883, help='')
    parser.add_argument('-redis_host', '--redis_host', default='192.168.3.56', help='')
    
    args = parser.parse_args()
    
    pool = redis.ConnectionPool(host=args.redis_host)  # 实现一个连接池
    r = redis.Redis(connection_pool=pool)  
    
    startServer()
