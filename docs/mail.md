# 1. 邮件发送模块 (`mail.py`)

## 1.1 `EmailSender` 类

**目的**: 发送电子邮件，支持HTML和附件。

## 初始化 (`__init__`)
- **参数**:
  - `username`: 发件人邮箱用户名。
  - `password`: 发件人邮箱密码。
  - `smtpserver`: SMTP服务器地址，默认为`"smtp.163.com"`。
  - `port`: SMTP服务端口，默认为`587`。
  - `nickname`: 发件人昵称，默认为`"PYXBOX-邮件工具"`。

- **用法**:
  ```python
  sender = EmailSender('your_username', 'your_password')
  ```

## 上下文管理 (`__enter__` 和 `__exit__`)
- **目的**: 管理邮件发送会话，自动登录和退出SMTP服务。

- **用法**:
  ```python
  with EmailSender('your_username', 'your_password') as sender:
      # 发送邮件代码
  ```

## 登录 (`login`)
- **目的**: 连接并登录到SMTP服务器。

- **用法**: 在`with`语句中自动调用。

## 发送邮件 (`send`)
- **参数**:
  - `receivers`: 收件人邮箱列表。
  - `subject`: 邮件主题。
  - `content`: 邮件内容。
  - `cc_recipients`: 抄送人邮箱列表。
  - `content_type`: 内容类型，"html"或"plain"。
  - `filepath`: 附件文件路径。

- **用法**:
  ```python
  sender.send(
      receivers=['receiver@example.com'],
      subject='Test Subject',
      content='Hello, this is a test email.',
      filepath='/path/to/attachment.pdf'
  )
  ```

## 退出 (`quit`)
- **目的**: 断开与SMTP服务器的连接。

- **用法**: 在`with`语句结束时自动调用。