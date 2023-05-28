# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2023/5/28 21:13
# @Author : BruceLong
# @FileName: media.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import base64
import logging
import os
from typing import Optional, Dict

import ffmpeg
from tqdm import tqdm
from .tools import x_file
import requests


# *********************************************** 视频类工具 --start ***********************************************

class Video:
    def __init__(self):
        pass

    def download(self, url: str, save_path: str, proxies: Optional[Dict[str, None]] = None,
                 data: Optional[Dict[str, None]] = None, **kwargs):
        '''
        url:文件的 URL
        save_path:保存文件的路径
        proxies:{'http':"http://127.0.0.1:21882",'https':"http://127.0.0.1:21882"}
        data = {
            'key1': 'value1',
            'key2': 'value2'
        }
        '''
        directory = os.path.dirname(save_path)
        x_file.makedirs_file_path(directory)
        # 发送带有 stream=True 参数的 GET 请求,带有代理和数据的 GET 请求
        response = requests.get(url, stream=True, proxies=proxies, data=data, **kwargs)
        # 检查响应状态码是否为 200 OK
        if response.status_code == 200:
            total_size = int(response.headers.get('Content-Length', 0))
            block_size = 1024  # 每次下载的块大小
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

            with open(save_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

            progress_bar.close()
            logging.info("File downloaded successfully.")
        else:
            logging.info("Failed to download file.")

    def convert_video(self, input_file, output_file, output_format):
        if any([x_file.is_exist(input_file), output_file, output_format]):
            logging.info('缺少参数')
        else:
            directory = os.path.dirname(output_file)
            x_file.makedirs_file_path(directory)
            try:
                ffmpeg.input(input_file).output(output_file, format=output_format).run()
                logging.info('格式转换完成')
            except ffmpeg.Error as e:
                logging.error(f"视频格式转换失败: {e.stderr.decode()}")


x_video = Video()


# *********************************************** 视频类工具 --end ***********************************************

# *********************************************** 图片类工具 --start ***********************************************

class Image:
    def __init__(self):
        pass

    def base64_to_jpg(self, b64str, save_path):
        data = base64.b64decode(b64str)
        directory = os.path.dirname(save_path)
        x_file.makedirs_file_path(directory)
        with open(''.format(save_path), 'wb') as f:
            f.write(data)
            return save_path

    def jpg_to_base64(self, jpg_path):
        if any([x_file.is_exist(jpg_path)]):
            logging.info('请输入正确的文件路径')
        else:
            with open(jpg_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                return encoded_string.decode("utf-8")


x_image = Image()


# *********************************************** 图片类工具 --end ***********************************************


# *********************************************** 声音类工具 --end ***********************************************
class Sound:
    def __init__(self):
        import whisper
        self.model = whisper.load_model("base")

    def get_mp3_text(self, input_file):
        result = self.model.transcribe(input_file)
        return result

# *********************************************** 声音类工具 --end ***********************************************
