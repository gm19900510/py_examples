# -*- coding:utf-8 -*-
from urllib import parse
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

         
def handle(r, args, path):
    return_data = ""
    url_path, param_data = urlparse(path)  # 处理URL请求参数，根据参数获取相应数据
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
            
            if r.exists(process_id): 
                process_num = int(str(r.get(process_id), encoding="utf-8"))
                print('用户执行播放停止操作，存在转换进程，当前转换进程数：', process_num) 
                if process_num == 1:
                    print('删除码流转换进程键值对：' + process_id)  
                    r.delete(process_id)
                else:    
                    r.setex(process_id, 60 * 60 * 1, (process_num - 1)) 
                    print('更新码流转换进程键值对：' + process_id, (process_num - 1))  
            else:
                print('流转换进程键值对不存在') 
        
        except Exception as e:
            print('traceback.print_exc():', traceback.print_exc(), e)     
     
    return return_data
