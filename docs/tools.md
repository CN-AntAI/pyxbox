# 5. 工具模块 (`tools.py`)

# 5.1 文件操作类 (`File`)

## 删除文件或目录 (`rm_files`)
- **目的**: 删除指定的文件或目录列表。

- **参数**:
  - `basedir`: 基础路径。
  - `filenames`: 要删除的文件或目录列表。

- **用法**:
  ```python
  x_file.rm_files(basedir='/path/to/dir', filenames=['file1.txt', 'dir1'])
  ```

## 根据创建时间排序文件 (`get_mtime_files`)
- **目的**: 根据文件的创建时间进行排序，并可选择删除旧文件。

- **参数**:
  - `basedir`: 基础路径。
  - `limit`: 保留的文件数量。
  - `is_rm`: 是否删除旧文件。

- **用法**:
  ```python
  x_file.get_mtime_files(basedir='/path/to/dir', limit=10, is_rm=True)
  ```

## 创建目录 (`mkdir`)
- **目的**: 创建指定路径的目录。

- **参数**:
  - `path`: 要创建的目录路径。

- **用法**:
  ```python
  x_file.mkdir('/path/to/newdir')
  ```

## 写入文件 (`write_file`)
- **目的**: 将内容写入文件。

- **参数**:
  - `filename`: 文件名及路径。
  - `content`: 要写入的内容。
  - `mode`: 写入模式，"w"为覆盖，"w+"为追加。
  - `encoding`: 文件编码。

- **用法**:
  ```python
  x_file.write_file('example.txt', 'Hello, world!', mode='w', encoding='utf-8')
  ```

## 读取文件 (`read_file`)
- **目的**: 从
文件中读取内容。

- **参数**:
  - `filename`: 文件名及路径。
  - `readlines`: 是否按行读取。
  - `encoding`: 文件编码。

- **用法**:
  ```python
  content = x_file.read_file('example.txt', readlines=True)
  ```

## 下载文件 (`download_file`)
- **目的**: 从网络下载文件。

- **参数**:
  - `url`: 文件的URL。
  - `file_path`: 本地保存路径。
  - `call_func`: 下载成功后的回调函数。
  - `proxies`: 代理配置。

- **用法**:
  ```python
  def download_callback():
      print('Download completed!')

  x_file.download_file('http://example.com/file.zip', 'local_file.zip', call_func=download_callback)
  ```

## 获取文件列表 (`get_file_list`)
- **目的**: 递归获取指定路径下的所有文件列表。

- **参数**:
  - `path`: 搜索路径。
  - `ignore`: 忽略的文件或目录列表。

- **用法**:
  ```python
  file_list = x_file.get_file_list('/path/to/search', ignore=['dir_to_ignore'])
  ```

# 5.2 日期时间类 (`DateTime`)

## 时间戳转日期 (`date_to_timestamp`)
- **目的**: 将日期字符串转换为时间戳。

- **参数**:
  - `date`: 日期字符串。
  - `time_format`: 日期格式。

- **用法**:
  ```python
  timestamp = x_datetime.date_to_timestamp('2024-07-02 12:00:00')
  ```

## 日期转时间戳 (`timestamp_to_date`)
- **目的**: 将时间戳转换回日期字符串。

- **参数**:
  - `timestamp`: 时间戳。
  - `time_format`: 输出日期的格式。

- **用法**:
  ```python
  date_str = x_datetime.timestamp_to_date(1672636400, '%Y-%m-%d %H:%M:%S')
  ```

## 获取当前时间戳 (`get_current_timestamp`)
- **目的**: 获取当前时间的时间戳。

- **用法**:
  ```python
  current_timestamp = x_datetime.get_current_timestamp()
  ```

## 获取当前日期 (`get_current_date`)
- **目的**: 获取当前日期字符串。

- **参数**:
  - `date_format`: 输出日期的格式。

- **用法**:
  ```python
  current_date = x_datetime.get_current_date('%Y-%m-%d %H:%M:%S')
  ```

# 5.3 网络操作类 (`NET`)

## 静态资源临时服务器 (`static_src_temp_server`)
- **目的**: 启动一个临时的静态资源服务器，用于快速访问本地资源。

- **参数**:
  - `server_name`: 服务器名称。
  - `full_path`: 资源所在的完整路径。
  - `port`: 服务器端口，默认为`8888`。

- **用法**:
  ```python
  server_info = x_net.static_src_temp_server('temp_server', '/path/to/resources', 8080)
  ```

# 5.4 加密类 (`MM`)

## 获取MD5哈希 (`get_md5`)
- **目的**: 生成MD5哈希值。

- **参数**:
  - 任意数量的字符串参数，将它们连接后生成MD5。

- **用法**:
  ```python
  md5_hash = x_mm.get_md5('hello', 'world')
  ```

## 获取SHA1哈希 (`get_sha1`)
- **目的**: 生成SHA1哈希值。

- **参数**:
  - 任意数量的字符串参数，将它们连接后生成SHA1。

- **用法**:
  ```python
  sha1_hash = x_mm.get_sha1('hello', 'world')
  ```

## Base64编码 (`get_base64`)
- **目的**: 对消息进行Base64编码。

- **参数**:
  - `secret`: 密钥。
  - `message`: 需要编码的消息。

- **用法**:
  ```python
  base64_encoded = x_mm.get_base64('my_secret_key', 'hello world')
  ```

## 生成UUID (`get_uuid`)
- **目的**: 生成UUID。

- **参数**:
  - `key1`, `key2`: 两个键，用于生成唯一的UUID。

- **用法**:
  ```python
  uuid_value = x_mm.get_uuid('domain_name', 'resource_name')
  ```

# 5.5 其他工具函数

## 获取随机密码 (`get_random_password`)
- **目的**: 生成随机密码。

- **参数**:
  - `length`: 密码长度。
  - `special_characters`: 密码中包含的特殊字符。

- **用法**:
  ```python
  password = x_faker.get_random_password(12, '!@#$%^&*')
  ```

## 获取随机邮箱 (`get_random_email`)
- **目的**: 生成随机邮箱地址。

- **参数**:
  - `length`: 邮箱用户名长度。
  - `email_types`: 邮箱域名列表。

- **用法**:
  ```python
  email = x_faker.get_random_email(length=10)
  ```