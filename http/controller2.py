# -*- coding:utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
from urllib import parse
import redis
from tools.transcode_tool import TranscodeTool
import traceback
from multiprocessing import Process


# 解析URL
def urlparse(path):
    # url解码
    urldata = parse.unquote(path)
    # url结果  
    result = parse.urlparse(urldata) 
    # url里的查询参数  
    query_dict = parse.parse_qs(result.query)
    return result.path, query_dict


def transcodeHandle(args, device):
    transcode = TranscodeTool(args)  
    transcode.trans(device)

     
class HTTPTool(BaseHTTPRequestHandler): 
    '''
    def __init__(self, args): 
        self.pool = redis.ConnectionPool(host=args.redis_host)  # 实现一个连接池
        self.r = redis.Redis(connection_pool=self.pool)  
        self.args = args
    '''
        
    def do_GET(self):
        self.pool = redis.ConnectionPool(host=args.redis_host)  # 实现一个连接池
        self.r = redis.Redis(connection_pool=self.pool)  
        
        return_data = ""
        url_path, param_data = urlparse(self.path)  # 处理URL请求参数，根据参数获取相应数据
        print(url_path, param_data)  
        
        device = param_data["name"][0]
        
        if url_path == "/v1/rtmp/on_play":
            return_data = "on_play"
            
            try :
                c1 = Process(target=transcodeHandle, args=(args, device))
                c1.start() 
            except Exception as e:
                print('traceback.print_exc():', traceback.print_exc(), e)        
        
        elif url_path == "/v1/rtmp/on_play_done":
            return_data = "on_play_done"
            try :
                process_id = 'process_id_' + device
                
                if self.r.exists(process_id): 
                    process_num = int(str(self.r.get(process_id), encoding="utf-8"))
                    print('用户执行播放停止操作，存在转换进程，当前转换进程数：', process_num) 
                    if process_num == 1:
                        print('删除码流转换进程键值对：' + process_id)  
                        self.r.delete(process_id)
                    else:    
                        self.r.setex(process_id, 60 * 60 * 1, (process_num - 1)) 
                        print('更新码流转换进程键值对：' + process_id, (process_num - 1))  
                else:
                    print('流转换进程键值对不存在') 
            
            except Exception as e:
                print('traceback.print_exc():', traceback.print_exc(), e)     
         
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
    
    startServer()
