# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2023/5/29 9:31
# @Author : BruceLong
# @FileName: mail.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import logging
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class EmailSender(object):
    def __init__(self, username, password, smtpserver="smtp.163.com", port=587, nickname='PYXBOX-邮件工具'):
        self.username = username
        self.password = password
        self.smtpserver = smtpserver
        self.smtp_client = smtplib.SMTP(smtpserver, port)
        self.nickname = nickname

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def quit(self):
        self.smtp_client.quit()

    def login(self):  # 开启 TLS 加密
        self.smtp_client.starttls()
        self.smtp_client.login(self.username, self.password)

    def send(
            self,
            receivers: list,
            subject: str = '【测试】来自pyxbox工具',
            content: str = '测试邮件',
            cc_recipients: list = None,
            content_type: str = "plain",
            filepath: str = None,
    ):
        """

        Args:
            receivers:收件人列表
            subject:主题
            content:内容
            content_type: 内容的类型html / plain
            filepath:文件路径

        Returns:

        """
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message["From"] = formataddr(
            (self.nickname, self.username)
        )  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        message["To"] = ",".join(
            [formataddr((receiver, receiver)) for receiver in receivers]
        )
        if cc_recipients:
            message["Cc"] = ",".join(cc_recipients)

        message["Subject"] = Header(subject, "utf-8")

        content = MIMEText(content, content_type, "utf-8")
        message.attach(content)

        # 构造附件
        if filepath:
            attach = MIMEText(open(filepath, "rb").read(), "base64", "utf-8")
            attach.add_header(
                "content-disposition",
                "attachment",
                filename=("utf-8", "", os.path.basename(filepath)),
            )
            message.attach(attach)

        msg = message.as_string()
        # 此处直接发送多个邮箱有问题，改成一个个发送
        for receiver in receivers:
            logging.debug("发送邮件到 {}".format(receiver))
            self.smtp_client.sendmail(self.username, receiver, msg)
        logging.debug("邮件发送成功！！！")
        return True


