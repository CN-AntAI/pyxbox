# pyxbox

## 介绍

万能工具库集合

## 架构图
![tools.png](http://tva1.sinaimg.cn/large/9aec9ebdgy1h0afusad7hj2e6k2dinpg.jpg)
### 软件架构功能说明
#### tools
- 时间相关工具模块
- SQL构造模块
- IP相关模块
- B站转码模块
- 微博id&mid互转
- 网络模块
- CMD命令行模块
- python常用加密模块
- 假数据生成模块
- Cookie相关模块
- 文本处理模块
- 文件相关模块
- URL处理相关模块
- Json处理相关模块
- HTML处理相关模块

#### media
##### video
- 视频的下载
- mp4转换为mp3
##### image
- base64toimage
- imagetobase64
- imageOCR
##### sound
- sound2str

#### user_agent
- 请求头：user-agent库

#### proxies
- 代理相关模块封装

#### mail
##### EmailSender
> 邮件发送工具，不用再写太多冗余的代码只需要简单的几行代码即可批量发送内容。

## 安装教程

1. 安装：`pip install pyxbox`
2. 更新：`pip install -U pyxbox`
3. 卸载：`pip uninstall pyxbox`

## 使用说明

## 新增功能
### 0.0.5
- 新增b站bv和av的转码
- 获取弹幕字节流的转码

### 0.1.4
> 更新时间为：2023年8月17日
- 新增微博的帖子id与mid相互转换
