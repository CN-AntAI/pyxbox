Bilibili平台相关的一些功能。以下是对这些代码的配置和功能的简要说明：

# #类变量
- `XOR_CODE`: 一个用于AV号和BV号转换的异或码。
- `MASK_CODE`: 一个用于AV号和BV号转换的掩码码。
- `MAX_AID`: AV号的最大值，用于计算。
- `ALPHABET`: 用于BV号编码的字符集。
- `ENCODE_MAP` 和 `DECODE_MAP`: 用于BV号编码和解码的映射表。
- `BASE`: 编码基础，即字符集的大小。
- `PREFIX`: BV号的前缀。
- `PREFIX_LEN`: BV号前缀的长度。
- `CODE_LEN`: 编码映射表的长度。

## 方法
- `bv_to_av(bvd: str) -> int`: 将BV号转换为AV号。
- `av_to_bv(avd: int) -> str`: 将AV号转换为BV号。
- `decode_view(stream: bytes)`: 解析弹幕的视图函数，处理二进制流并返回JSON格式的数据。
  - `read_dm_seg(stream: bytes)`: 读取弹幕分段数据。
  - `read_flag(stream: bytes)`: 读取弹幕标志数据。
  - `read_command_danmakus(stream: bytes)`: 读取命令弹幕数据。
  - `read_settings(stream: bytes)`: 读取弹幕设置数据。
- `decode_danmakus(stream: bytes)`: 解析弹幕数据，将二进制流转换为弹幕对象列表。

## 异常处理
- `DanmakuClosedException`: 当尝试解析的弹幕数据表示视频弹幕被关闭时抛出的异常。

## 使用示例
```python
x_bilibili = Bilibili()  # 创建Bilibili类的实例
av_number = x_bilibili.bv_to_av("BV1xX41197sN")  # 将BV号转换为AV号
bv_number = x_bilibili.av_to_bv(123456789)  # 将AV号转换为BV号
```

## 注意事项
- 确保传入的BV号是正确的格式，即以 `BV1` 开头。
- 转换函数使用了类变量作为转换的基础，这些变量定义了转换算法的核心逻辑。
- 解码函数 `decode_view` 和 `decode_danmakus` 需要传入二进制流作为参数，这些函数将解析这些数据并返回相应的结构化信息。
