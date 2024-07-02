 # 2. 媒体处理模块 (`media.py`)

# 2.1 `Video` 类

## 下载视频 (`download`)
- **目的**: 从网络下载视频文件。

- **参数**:
  - `url`: 视频文件的URL。
  - `save_path`: 保存视频的本地路径。

- **用法**:
  ```python
  x_video.download('http://example.com/video.mp4', 'local_video.mp4')
  ```

## 转换视频格式 (`convert_video`)
- **目的**: 将视频文件转换为另一种格式。

- **参数**:
  - `input_file`: 输入视频文件路径。
  - `output_file`: 输出视频文件路径。
  - `output_format`: 输出视频格式。

- **用法**:
  ```python
  x_video.convert_video('video.mp4', 'output.avi', 'avi')
  ```

# 2.2 `Image` 类

## Base64转JPG (`base64_to_jpg`)
- **目的**: 将Base64编码的字符串转换为JPG图片文件。

- **参数**:
  - `b64str`: Base64编码的字符串。
  - `save_path`: 保存图片的本地路径。

- **用法**:
  ```python
  x_image.base64_to_jpg(base64_string, 'output_image.jpg')
  ```

## JPG转Base64 (`jpg_to_base64`)
- **目的**: 将JPG图片文件转换为Base64编码的字符串。

- **参数**:
  - `jpg_path`: JPG图片文件路径。

- **用法**:
  ```python
  base64_data = x_image.jpg_to_base64('input_image.jpg')
  ```

# 2.3 `Sound` 类

## 获取MP3文本 (`get_mp3_text`)
- **目的**: 从MP3音频文件中提取文本内容。

- **参数**:
  - `input_file`: MP3文件路径。

- **用法**:
  ```python
  text = x_sound.get_mp3_text('audio.mp3')
  ```