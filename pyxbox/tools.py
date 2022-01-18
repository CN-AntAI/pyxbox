# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/1/18 16:01
# @Author : BruceLong
# @FileName: tools.py
# @Email   : 18656170559@163.com
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import calendar
import datetime
import functools
import hashlib
import html
import json
import logging
import os
import random
import re
import shutil
import socket
import string
import time
import traceback
import urllib
import uuid
from pprint import pformat
from urllib.parse import urljoin, urlencode

import requests
from requests.cookies import RequestsCookieJar
from w3lib.url import canonicalize_url as _canonicalize_url


# *********************************************** 普通工具 --start ***********************************************
def get_host_info():
    '''
    获取主机相关信息
    :return:
    '''
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    result = {
        'ip': ip,
        'hostname': hostname,  # 主机名
        'sys_type': os.name,  # 当前只注册了3个值：分别是posix , nt , java， 对应linux/windows/java虚拟机
    }
    return result


def run_safe_model(module_name):
    def inner_run_safe_model(func):
        try:
            @functools.wraps(func)  # 将函数的原来属性付给新函数
            def run_func(*args, **kw):
                callfunc = None
                try:
                    callfunc = func(*args, **kw)
                except Exception as e:
                    logging.error(module_name + ": " + func.__name__ + " - " + str(e))
                    traceback.print_exc()
                return callfunc

            return run_func
        except Exception as e:
            logging.error(module_name + ": " + func.__name__ + " - " + str(e))
            traceback.print_exc()
            return func

    return inner_run_safe_model


# ************************************************ 普通工具 --end ************************************************
# ************************************************ CMD命令相关模块 --start ************************************************

class CMD:
    def kill_linux_process(self, port: int = None, pid: int = None, keyword: str = None):
        '''
                杀死linux进程
                :param port:根据端口号杀死
                :param pid: 根据pid号杀死
                :param keyword: 根据关键词杀死
                :return:
                '''
        if port:
            os.popen(f"kill $(lsof -Pti :{port})")
        if pid:
            os.popen(f"sudo kill -9 {pid}")
        if keyword:
            os.popen("ps auxww | grep {keyword} | awk '{p}' | xargs kill -9".format(keyword=keyword, p='{print $2}'))


x_cmd = CMD()


# ************************************************ CMD命令相关模块 --end ************************************************

# *********************************************** 网络相关模块 --start ***********************************************
class NET:
    def static_src_temp_server(self, server_name: str, full_path: str = None, port: int = 8888) -> dict:
        '''
        静态资源临时访问服务
        :param full_path:绝对路径
        :param port: 端口号
        :return: 结果信息
        '''
        sys_type = get_host_info().get('sys_type')

        # 1. 判断目录是否存在
        msg = {'msg': '一切ok'}
        if not os.path.exists(full_path):
            msg['path_msg'] = '路径不存在，请传入正确的路径'
        # 3. 获取当前ip地址
        ip = get_host_info().get('ip')
        # 系统类型为windows操作系统做以下操作
        if sys_type == 'nt':
            # 4. cmd进入文件目录
            # 2. 判断对应端口是否存在
            port_status = os.popen(f'netstat -ano|findstr "{port}"').read().split('\n')
            if port_status[0]:
                msg['port_msg'] = '抱歉端口已经被占用'
            # 5. 启动对应的服务
            server_path = x_file.makedirs_file_path(dir_name='cmd')
            run_str = f'''@echo off
        if "%1" == "h" goto begin
        mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit
        :begin
        cd "{full_path}" && python -m http.server {port}'''
            filename = f'{server_name}_start.bat'
            save_file_path = os.path.join(server_path, filename)
            with open(save_file_path, 'w') as f:
                f.write(run_str)
            os.popen(f'''cd {server_path} && {filename}''').read().split('\n')
        # 系统类型为linux操作系统做以下操作
        if sys_type == 'posix':
            port_status = os.popen(f'netstat -an|grep "{port}"').read().split('\n')
            if port_status[0]:
                msg['port_msg'] = '抱歉端口已经被占用'
                # 慎用
                # kill_linux_process(port=port)
            os.popen(f'''cd "{full_path}" && python -m http.server {port} > /dev/null 2>&1 &''').read().split('\n')
        return dict(
            {
                'ip': ip,
                'port': port,
                'httpserver': f'http://{ip}:{port}'
            }
            , **msg
        )


x_net = NET()


# ************************************************ 网络相关模块 --end ************************************************
# *********************************************** 文件相关模块 --start ***********************************************
class File:
    def rm_files(self, basedir: str = None, filenames: list = None):
        '''
        删除文件列表
        :param basedir:基础文件路径
        :param filenames: 文件列表
        :return:
        '''
        if basedir:
            filenames = [os.path.join(basedir, i) for i in filenames]
        # 判断是文件还是文件夹, 若是文件夹 全部删除  若是文件 跳过
        for _ in filenames:
            if os.path.isdir(_):  # 判断是否为文件夹
                # **注：该命令可递归删除文件夹,慎用!!该文件夹和文件夹里面所有内容会被删除.
                shutil.rmtree(_)
                print("%s目录 已删除" % _)
            else:  # 如果不是文件夹,则为文件
                os.remove(_)  # 该命令删除文件
                print("%s文件 已删除" % _)

    def get_mtime_files(self, basedir: str = None, limit: int = 1000, is_rm: bool = False):
        '''
        根据创建时间倒序，并确定是否需要删除文件
        :param basedir: 基础文件路径
        :param limit: 注注注：需要保留的文件数
        :param is_rm: 是否需要删除
        :return:
        '''
        lists = os.listdir(basedir)
        # 按文件创建时间正序排列
        lists.sort(key=lambda fn: os.path.getmtime(basedir + '\\' + fn))
        if is_rm:
            print(lists[:-limit])
            x = input('确定是否删除【0/1】：')
            if x == '1':
                # print('所有文件已经删除完毕')
                self.rm_files(basedir=basedir, filenames=lists)
        # print(lists[:limit])

    def mkdir(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError as exc:  # Python >2.5
            pass

    def write_file(self, filename, content, mode="w", encoding="utf-8"):
        """
        @summary: 写文件
        ---------
        @param filename: 文件名（有路径）
        @param content: 内容
        @param mode: 模式 w/w+ (覆盖/追加)
        ---------
        @result:
        """

        directory = os.path.dirname(filename)
        self.mkdir(directory)
        with open(filename, mode, encoding=encoding) as file:
            file.writelines(content)

    def read_file(self, filename, readlines=False, encoding="utf-8"):
        """
        @summary: 读文件
        ---------
        @param filename: 文件名（有路径）
        @param readlines: 按行读取 （默认False）
        ---------
        @result: 按行读取返回List，否则返回字符串
        """

        content = None
        try:
            with open(filename, "r", encoding=encoding) as file:
                content = file.readlines() if readlines else file.read()
        except Exception as e:
            logging.error(e)

        return content

    def get_oss_file_list(self, oss_handler, prefix, date_range_min, date_range_max=None):
        """
        获取文件列表
        @param prefix: 路径前缀 如 data/car_service_line/yiche/yiche_serial_zongshu_info
        @param date_range_min: 时间范围 最小值 日期分隔符为/ 如 2019/03/01 或 2019/03/01/00/00/00
        @param date_range_max: 时间范围 最大值 日期分隔符为/ 如 2019/03/01 或 2019/03/01/00/00/00
        @return: 每个文件路径 如 html/e_commerce_service_line/alibaba/alibaba_shop_info/2019/03/22/15/53/15/8ca8b9e4-4c77-11e9-9dee-acde48001122.json.snappy
        """

        # 计算时间范围
        date_range_max = date_range_max or date_range_min
        date_format = "/".join(
            ["%Y", "%m", "%d", "%H", "%M", "%S"][: date_range_min.count("/") + 1]
        )
        time_interval = [
            {"days": 365},
            {"days": 31},
            {"days": 1},
            {"hours": 1},
            {"minutes": 1},
            {"seconds": 1},
        ][date_range_min.count("/")]
        date_range = x_datetime.get_between_date(
            date_range_min, date_range_max, date_format=date_format, **time_interval
        )

        for date in date_range:
            file_folder_path = os.path.join(prefix, date)
            objs = oss_handler.list(prefix=file_folder_path)
            for obj in objs:
                filename = obj.key
                yield filename

        pass

    def is_exist(self, file_path):
        """
        @summary: 文件是否存在
        ---------
        @param file_path:
        ---------
        @result:
        """

        return os.path.exists(file_path)

    def makedirs_file_path(self, base_path: str = None, dir_name: str = '') -> str:
        '''
        根据给定的文件夹名，在当路径中创建相应的文件夹
        :param base_path: 基础文件夹路径
        :param dir_name: 需要创建的文件夹名
        :return: 创建完成后的文件夹路径
        '''
        path = os.path.dirname(__file__).replace('until', '')
        if base_path:
            path = base_path
        file_path = os.path.join(path, dir_name).replace('\\', '/')

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return file_path


x_file = File()


# *********************************************** 文件相关模块 --end ***********************************************
# *********************************************** 日期时间相关模块 --start ***********************************************
class DateTime:
    def date_to_timestamp(self, date, time_format="%Y-%m-%d %H:%M:%S"):
        """
        @summary:
        ---------
        @param date:将"2011-09-28 10:00:00"时间格式转化为时间戳
        @param format:时间格式
        ---------
        @result: 返回时间戳
        """

        timestamp = time.mktime(time.strptime(date, time_format))
        return int(timestamp)

    def timestamp_to_date(self, timestamp, time_format="%Y-%m-%d %H:%M:%S"):
        """
        @summary:
        ---------
        @param timestamp: 将时间戳转化为日期
        @param format: 日期格式
        ---------
        @result: 返回日期
        """
        if timestamp is None:
            raise ValueError("timestamp is null")

        date = time.localtime(timestamp)
        return time.strftime(time_format, date)

    def get_current_timestamp(self):
        return int(time.time())

    def get_current_date(self, date_format="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.now().strftime(date_format)
        # return time.strftime(date_format, time.localtime(time.time()))

    def get_date_number(self, year=None, month=None, day=None):
        """
        @summary: 获取指定日期对应的日期数
        默认当前周
        ---------
        @param year: 2010
        @param month: 6
        @param day: 16
        ---------
        @result: (年号，第几周，第几天) 如 (2010, 24, 3)
        """
        if year and month and day:
            return datetime.date(year, month, day).isocalendar()
        elif not any([year, month, day]):
            return datetime.datetime.now().isocalendar()
        else:
            assert year, "year 不能为空"
            assert month, "month 不能为空"
            assert day, "day 不能为空"

    def get_between_date(self,
                         begin_date, end_date=None, date_format="%Y-%m-%d", **time_interval
                         ):
        """
        @summary: 获取一段时间间隔内的日期，默认为每一天
        ---------
        @param begin_date: 开始日期 str 如 2018-10-01
        @param end_date: 默认为今日
        @param date_format: 日期格式，应与begin_date的日期格式相对应
        @param time_interval: 时间间隔 默认一天 支持 days、seconds、microseconds、milliseconds、minutes、hours、weeks
        ---------
        @result: list 值为字符串
        """

        date_list = []

        begin_date = datetime.datetime.strptime(begin_date, date_format)
        end_date = (
            datetime.datetime.strptime(end_date, date_format)
            if end_date
            else datetime.datetime.strptime(
                time.strftime(date_format, time.localtime(time.time())), date_format
            )
        )
        time_interval = time_interval or dict(days=1)

        while begin_date <= end_date:
            date_str = begin_date.strftime(date_format)
            date_list.append(date_str)

            begin_date += datetime.timedelta(**time_interval)

        if end_date.strftime(date_format) not in date_list:
            date_list.append(end_date.strftime(date_format))

        return date_list

    def get_between_months(self, begin_date, end_date=None):
        """
        @summary: 获取一段时间间隔内的月份
        需要满一整月
        ---------
        @param begin_date: 开始时间 如 2018-01-01
        @param end_date: 默认当前时间
        ---------
        @result: 列表 如 ['2018-01', '2018-02']
        """

        def add_months(dt, months):
            month = dt.month - 1 + months
            year = dt.year + month // 12
            month = month % 12 + 1
            day = min(dt.day, calendar.monthrange(year, month)[1])
            return dt.replace(year=year, month=month, day=day)

        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = (
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
            if end_date
            else datetime.datetime.strptime(
                time.strftime("%Y-%m-%d", time.localtime(time.time())), "%Y-%m-%d"
            )
        )
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m")
            date_list.append(date_str)
            begin_date = add_months(begin_date, 1)
        return date_list

    def get_today_of_day(self, day_offset=0):
        return str(datetime.date.today() + datetime.timedelta(days=day_offset))

    def get_days_of_month(self, year, month):
        """
        返回天数
        """

        return calendar.monthrange(year, month)[1]

    def get_firstday_of_month(self, date):
        """''
        date format = "YYYY-MM-DD"
        """

        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)

        days = "01"
        if int(month) < 10:
            month = "0" + str(int(month))
        arr = (year, month, days)
        return "-".join("%s" % i for i in arr)

    def get_lastday_of_month(self, date):
        """''
        get the last day of month
        date format = "YYYY-MM-DD"
        """
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)

        days = calendar.monthrange(year, month)[1]
        month = self.add_zero(month)
        arr = (year, month, days)
        return "-".join("%s" % i for i in arr)

    def get_firstday_month(self, month_offset=0):
        """''
        get the first day of month from today
        month_offset is how many months
        """
        (y, m, d) = self.get_year_month_and_days(month_offset)
        d = "01"
        arr = (y, m, d)
        return "-".join("%s" % i for i in arr)

    def get_lastday_month(self, month_offset=0):
        """''
        get the last day of month from today
        month_offset is how many months
        """
        return "-".join("%s" % i for i in self.get_year_month_and_days(month_offset))

    def get_last_month(self, month_offset=0):
        """''
        get the last day of month from today
        month_offset is how many months
        """
        return "-".join("%s" % i for i in self.get_year_month_and_days(month_offset)[:2])

    def get_year_month_and_days(self, month_offset=0):
        """
        @summary:
        ---------
        @param month_offset: 月份偏移量
        ---------
        @result: ('2019', '04', '30')
        """

        today = datetime.datetime.now()
        year, month = today.year, today.month

        this_year = int(year)
        this_month = int(month)
        total_month = this_month + month_offset
        if month_offset >= 0:
            if total_month <= 12:
                days = str(self.get_days_of_month(this_year, total_month))
                total_month = self.add_zero(total_month)
                return (year, total_month, days)
            else:
                i = total_month // 12
                j = total_month % 12
                if j == 0:
                    i -= 1
                    j = 12
                this_year += i
                days = str(self.get_days_of_month(this_year, j))
                j = self.add_zero(j)
                return (str(this_year), str(j), days)
        else:
            if (total_month > 0) and (total_month < 12):
                days = str(self.get_days_of_month(this_year, total_month))
                total_month = self.add_zero(total_month)
                return (year, total_month, days)
            else:
                i = total_month // 12
                j = total_month % 12
                if j == 0:
                    i -= 1
                    j = 12
                this_year += i
                days = str(self.get_days_of_month(this_year, j))
                j = self.add_zero(j)
                return (str(this_year), str(j), days)

    def add_zero(self, n):
        return "%02d" % n

    def get_month(self, month_offset=0):
        """''
        获取当前日期前后N月的日期
        if month_offset>0, 获取当前日期前N月的日期
        if month_offset<0, 获取当前日期后N月的日期
        date format = "YYYY-MM-DD"
        """
        today = datetime.datetime.now()
        day = self.add_zero(today.day)

        (y, m, d) = self.get_year_month_and_days(month_offset)
        arr = (y, m, d)
        if int(day) < int(d):
            arr = (y, m, day)
        return "-".join("%s" % i for i in arr)

    @run_safe_model("format_date")
    def format_date(self, date, old_format="", new_format="%Y-%m-%d %H:%M:%S"):
        """
        @summary: 格式化日期格式
        ---------
        @param date: 日期 eg：2017年4月17日 3时27分12秒
        @param old_format: 原来的日期格式 如 '%Y年%m月%d日 %H时%M分%S秒'
            %y 两位数的年份表示（00-99）
            %Y 四位数的年份表示（000-9999）
            %m 月份（01-12）
            %d 月内中的一天（0-31）
            %H 24小时制小时数（0-23）
            %I 12小时制小时数（01-12）
            %M 分钟数（00-59）
            %S 秒（00-59）
        @param new_format: 输出的日期格式
        ---------
        @result: 格式化后的日期，类型为字符串 如2017-4-17 03:27:12
        """
        if not date:
            return ""

        if not old_format:
            regex = "(\d+)"
            numbers = x_text.get_info(date, regex, allow_repeat=True)
            formats = ["%Y", "%m", "%d", "%H", "%M", "%S"]
            old_format = date
            for i, number in enumerate(numbers[:6]):
                if i == 0 and len(number) == 2:  # 年份可能是两位 用小%y
                    old_format = old_format.replace(
                        number, formats[i].lower(), 1
                    )  # 替换一次 '2017年11月30日 11:49' 防止替换11月时，替换11小时
                else:
                    old_format = old_format.replace(number, formats[i], 1)  # 替换一次

        try:
            date_obj = datetime.datetime.strptime(date, old_format)
            if "T" in date and "Z" in date:
                date_obj += datetime.timedelta(hours=8)
                date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = datetime.datetime.strftime(date_obj, new_format)

        except Exception as e:
            logging.error("日期格式化出错，old_format = %s 不符合 %s 格式" % (old_format, date))
            date_str = date

        return date_str

    def transform_lower_num(self, data_str: str):
        num_map = {
            "一": "1",
            "二": "2",
            "两": "2",
            "三": "3",
            "四": "4",
            "五": "5",
            "六": "6",
            "七": "7",
            "八": "8",
            "九": "9",
            "十": "0",
        }
        pattern = f'[{"|".join(num_map.keys())}|零]'
        res = re.search(pattern, data_str)
        if not res:
            #  如果字符串中没有包含中文数字 不做处理 直接返回
            return data_str

        data_str = data_str.replace("0", "零")
        for n in num_map:
            data_str = data_str.replace(n, num_map[n])

        re_data_str = re.findall("\d+", data_str)
        for i in re_data_str:
            if len(i) == 3:
                new_i = i.replace("0", "")
                data_str = data_str.replace(i, new_i, 1)
            elif len(i) == 4:
                new_i = i.replace("10", "")
                data_str = data_str.replace(i, new_i, 1)
            elif len(i) == 2 and int(i) < 10:
                new_i = int(i) + 10
                data_str = data_str.replace(i, str(new_i), 1)
            elif len(i) == 1 and int(i) == 0:
                new_i = int(i) + 10
                data_str = data_str.replace(i, str(new_i), 1)

        return data_str.replace("零", "0")

    @run_safe_model("format_time")
    def format_time(self, release_time, date_format="%Y-%m-%d %H:%M:%S"):
        """
        # >>> format_time("2个月前")
        '2021-08-15 16:24:21'
        # >>> format_time("2月前")
        '2021-08-15 16:24:36'
        """
        release_time = self.transform_lower_num(release_time)
        release_time = release_time.replace("日", "天").replace("/", "-")

        if "年前" in release_time:
            years = re.compile("(\d+)\s*年前").findall(release_time)
            years_ago = datetime.datetime.now() - datetime.timedelta(
                days=int(years[0]) * 365
            )
            release_time = years_ago.strftime("%Y-%m-%d %H:%M:%S")

        elif "月前" in release_time:
            months = re.compile("(\d+)[\s个]*月前").findall(release_time)
            months_ago = datetime.datetime.now() - datetime.timedelta(
                days=int(months[0]) * 30
            )
            release_time = months_ago.strftime("%Y-%m-%d %H:%M:%S")

        elif "周前" in release_time:
            weeks = re.compile("(\d+)\s*周前").findall(release_time)
            weeks_ago = datetime.datetime.now() - datetime.timedelta(days=int(weeks[0]) * 7)
            release_time = weeks_ago.strftime("%Y-%m-%d %H:%M:%S")

        elif "天前" in release_time:
            ndays = re.compile("(\d+)\s*天前").findall(release_time)
            days_ago = datetime.datetime.now() - datetime.timedelta(days=int(ndays[0]))
            release_time = days_ago.strftime("%Y-%m-%d %H:%M:%S")

        elif "小时前" in release_time:
            nhours = re.compile("(\d+)\s*小时前").findall(release_time)
            hours_ago = datetime.datetime.now() - datetime.timedelta(hours=int(nhours[0]))
            release_time = hours_ago.strftime("%Y-%m-%d %H:%M:%S")

        elif "分钟前" in release_time:
            nminutes = re.compile("(\d+)\s*分钟前").findall(release_time)
            minutes_ago = datetime.datetime.now() - datetime.timedelta(
                minutes=int(nminutes[0])
            )
            release_time = minutes_ago.strftime("%Y-%m-%d %H:%M:%S")

        elif "前天" in release_time:
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=2)
            release_time = release_time.replace("前天", str(yesterday))

        elif "昨天" in release_time:
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            release_time = release_time.replace("昨天", str(yesterday))

        elif "今天" in release_time:
            release_time = release_time.replace("今天", self.get_current_date("%Y-%m-%d"))

        elif "刚刚" in release_time:
            release_time = self.get_current_date()

        elif re.search("^\d\d:\d\d", release_time):
            release_time = self.get_current_date("%Y-%m-%d") + " " + release_time

        elif not re.compile("\d{4}").findall(release_time):
            month = re.compile("\d{1,2}").findall(release_time)
            if month and int(month[0]) <= int(self.get_current_date("%m")):
                release_time = self.get_current_date("%Y") + "-" + release_time
            else:
                release_time = str(int(self.get_current_date("%Y")) - 1) + "-" + release_time

        # 把日和小时粘在一起的拆开
        template = re.compile("(\d{4}-\d{1,2}-\d{2})(\d{1,2})")
        release_time = re.sub(template, r"\1 \2", release_time)
        release_time = self.format_date(release_time, new_format=date_format)

        return release_time

    def to_date(self, date_str, date_format="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strptime(date_str, date_format)

    def get_before_date(self,
                        current_date,
                        days,
                        current_date_format="%Y-%m-%d %H:%M:%S",
                        return_date_format="%Y-%m-%d %H:%M:%S",
                        ):
        """
        @summary: 获取之前时间
        ---------
        @param current_date: 当前时间 str类型
        @param days: 时间间隔 -1 表示前一天 1 表示后一天
        @param days: 返回的时间格式
        ---------
        @result: 字符串
        """

        current_date = self.to_date(current_date, current_date_format)
        date_obj = current_date + datetime.timedelta(days=days)
        return datetime.datetime.strftime(date_obj, return_date_format)

    def delay_time(self, sleep_time=60):
        """
        @summary: 睡眠  默认1分钟
        ---------
        @param sleep_time: 以秒为单位
        ---------
        @result:
        """

        time.sleep(sleep_time)

    def format_seconds(self, seconds):
        """
        @summary: 将秒转为时分秒
        ---------
        @param seconds:
        ---------
        @result: 2天3小时2分49秒
        """

        seconds = int(seconds + 0.5)  # 向上取整

        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        times = ""
        if d:
            times += "{}天".format(d)
        if h:
            times += "{}小时".format(h)
        if m:
            times += "{}分".format(m)
        if s:
            times += "{}秒".format(s)

        return times


x_datetime = DateTime()


# *********************************************** 日期时间相关模块 --end ***********************************************
# *********************************************** Cookie相关模块 --start ***********************************************
class Cookie:
    """
                Cookie相关工具
                """

    def get_cookies(self, response):
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        return cookies

    def cookies_to_dict(self, cookie_str: str) -> dict:
        """
                                # >>> get_cookies_from_str("key=value; key2=value2; key3=; key4=; ")
                                {'key': 'value', 'key2': 'value2', 'key3': '', 'key4': ''}

                                Args:
                                    cookie_str: key=value; key2=value2; key3=; key4=

                                Returns:

                                """
        cookies = {}
        for cookie in cookie_str.split(";"):
            cookie = cookie.strip()
            if not cookie:
                continue
            key, value = cookie.split("=", 1)
            key = key.strip()
            value = value.strip()
            cookies[key] = value

        return cookies

    def get_cookies_jar(self, cookies):
        """
                                @summary: 适用于selenium生成的cookies转requests的cookies
                                requests.get(xxx, cookies=jar)
                                参考：https://www.cnblogs.com/small-bud/p/9064674.html

                                ---------
                                @param cookies: [{},{}]
                                ---------
                                @result: cookie jar
                                """

        cookie_jar = RequestsCookieJar()
        for cookie in cookies:
            cookie_jar.set(cookie["name"], cookie["value"])

        return cookie_jar

    def get_cookies_from_selenium_cookie(self, cookies):
        """
                                @summary: 适用于selenium生成的cookies转requests的cookies
                                requests.get(xxx, cookies=jar)
                                参考：https://www.cnblogs.com/small-bud/p/9064674.html

                                ---------
                                @param cookies: [{},{}]
                                ---------
                                @result: cookie jar
                                """

        cookie_dict = {}
        for cookie in cookies:
            if cookie.get("name"):
                cookie_dict[cookie["name"]] = cookie["value"]

        return cookie_dict

    def cookiesjar2str(self, cookies):
        str_cookie = ""
        for k, v in requests.utils.dict_from_cookiejar(cookies).items():
            str_cookie += k
            str_cookie += "="
            str_cookie += v
            str_cookie += "; "
        return str_cookie

    def cookies2str(self, cookies):
        str_cookie = ""
        for k, v in cookies.items():
            str_cookie += k
            str_cookie += "="
            str_cookie += v
            str_cookie += "; "
        return str_cookie


x_cookie = Cookie()


# ************************************************ Cookie相关模块 --end ************************************************

# *********************************************** 生成假数据相关模块 --start ***********************************************
class Faker:
    def get_random_password(self, length=8, special_characters=""):
        """
        @summary: 创建随机密码 默认长度为8，包含大写字母、小写字母、数字
        ---------
        @param length: 密码长度 默认8
        @param special_characters: 特殊字符
        ---------
        @result: 指定长度的密码
        """

        while True:
            random_password = "".join(
                random.sample(
                    string.ascii_letters + string.digits + special_characters, length
                )
            )
            if (
                    re.search("[0-9]", random_password)
                    and re.search("[A-Z]", random_password)
                    and re.search("[a-z]", random_password)
            ):
                if not special_characters:
                    break
                elif set(random_password).intersection(special_characters):
                    break

        return random_password

    def get_random_email(self, length=None, email_types: list = None, special_characters=""):
        """
        随机生成邮箱
        :param length: 邮箱长度
        :param email_types: 邮箱类型
        :param special_characters: 特殊字符
        :return:
        """
        if not length:
            length = random.randint(4, 12)
        if not email_types:
            email_types = [
                "qq.com",
                "163.com",
                "gmail.com",
                "yahoo.com",
                "hotmail.com",
                "yeah.net",
                "126.com",
                "139.com",
                "sohu.com",
            ]

        email_body = self.get_random_password(length, special_characters)
        email_type = random.choice(email_types)

        email = email_body + "@" + email_type
        return email


x_faker = Faker()


# ************************************************ 生成假数据相关模块 --end ************************************************
# *********************************************** URL相关模块 --start ***********************************************
class URL:
    def get_urls(
            self,
            html,
            stop_urls=(
                    "javascript",
                    "+",
                    ".css",
                    ".js",
                    ".rar",
                    ".xls",
                    ".exe",
                    ".apk",
                    ".doc",
                    ".jpg",
                    ".png",
                    ".flv",
                    ".mp4",
            ),
    ):
        # 不匹配javascript、 +、 # 这样的url
        regex = r'<a.*?href.*?=.*?["|\'](.*?)["|\']'

        urls = x_text.get_info(html, regex)
        urls = sorted(set(urls), key=urls.index)
        if stop_urls:
            stop_urls = isinstance(stop_urls, str) and [stop_urls] or stop_urls
            use_urls = []
            for url in urls:
                for stop_url in stop_urls:
                    if stop_url in url:
                        break
                else:
                    use_urls.append(url)

            urls = use_urls
        return urls

    def get_domain(self, url):
        proto, rest = urllib.parse.splittype(url)
        domain, rest = urllib.parse.splithost(rest)
        return domain

    def is_valid_url(self, url):
        """
        验证url是否合法
        :param url:
        :return:
        """
        if re.match(r"(^https?:/{2}\w.+$)|(ftp://)", url):
            return True
        else:
            return False

    def get_index_url(self, url):
        return "/".join(url.split("/")[:3])

    def get_full_url(self, root_url: str, sub_url: str):
        """
                    @summary: 得到完整的ur
                    ---------
                    @param root_url: 根url （网页的url）
                    @param sub_url:  子url （带有相对路径的 可以拼接成完整的）
                    ---------
                    @result: 返回完整的url
                    """

        return urljoin(root_url, sub_url)

    def join_url(self, url: str, params: str):
        # param_str = "?"
        # for key, value in params.items():
        #     value = isinstance(value, str) and value or str(value)
        #     param_str += key + "=" + value + "&"
        #
        # return url + param_str[:-1]

        if not params:
            return url

        params = urlencode(params)
        separator = "?" if "?" not in url else "&"
        return url + separator + params

    def canonicalize_url(self, url):
        """
                    url 归一化 会参数排序 及去掉锚点
                    """
        return _canonicalize_url(url)

    def get_url_md5(self, url):
        url = self.canonicalize_url(url)
        url = re.sub("^http://", "https://", url)
        return x_mm.get_md5(url)

    def fit_url(self, urls, identis):
        identis = isinstance(identis, str) and [identis] or identis
        fit_urls = []
        for link in urls:
            for identi in identis:
                if identi in link:
                    fit_urls.append(link)
        return list(set(fit_urls))

    def get_param(self, url, key):
        params = url.split("?")[-1].split("&")
        for param in params:
            key_value = param.split("=", 1)
            if key == key_value[0]:
                return key_value[1]
        return None

    def urlencode(self, params):
        """
                    字典类型的参数转为字符串
                    @param params:
                    {
                        'a': 1,
                        'b': 2
                    }
                    @return: a=1&b=2
                    """
        return urllib.parse.urlencode(params)

    def urldecode(self, url: str) -> dict:
        """
                    将字符串类型的参数转为json
                    @param url: xxx?a=1&b=2
                    @return:
                    {
                        'a': 1,
                        'b': 2
                    }
                    """
        params_json = {}
        params = url.split("?")[-1].split("&")
        for param in params:
            key, value = param.split("=")
            params_json[key] = self.unquote_url(value)

        return params_json

    def unquote_url(self, url: str, encoding="utf-8") -> str:
        """
                    @summary: 将url解码
                    ---------
                    @param url:
                    ---------
                    @result:
                    """

        return urllib.parse.unquote(url, encoding=encoding)

    def quote_url(self, url, encoding="utf-8"):
        """
                    @summary: 将url编码 编码意思http://www.w3school.com.cn/tags/html_ref_urlencode.html
                    ---------
                    @param url:
                    ---------
                    @result:
                    """

        return urllib.parse.quote(url, safe="%;/?:@&=+$,", encoding=encoding)


x_url = URL()


# ************************************************ URL相关模块 --end ************************************************


# *********************************************** 加密相关模块 --start ***********************************************
class MM:
    def get_md5(self, *args):
        """
        @summary: 获取唯一的32位md5
        ---------
        @param *args: 参与联合去重的值
        ---------
        @result: 7c8684bcbdfcea6697650aa53d7b1405
        """

        m = hashlib.md5()
        for arg in args:
            m.update(str(arg).encode())

        return m.hexdigest()

    def get_sha1(self, *args):
        """
        @summary: 获取唯一的40位值， 用于获取唯一的id
        ---------
        @param *args: 参与联合去重的值
        ---------
        @result: ba4868b3f277c8e387b55d9e3d0be7c045cdd89e
        """

        sha1 = hashlib.sha1()
        for arg in args:
            sha1.update(str(arg).encode())
        return sha1.hexdigest()  # 40位

    def get_base64(self, secret, message):
        """
        @summary: 数字证书签名算法是："HMAC-SHA256"
                  参考：https://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/
        ---------
        @param secret: 秘钥
        @param message: 消息
        ---------
        @result: 签名输出类型是："base64"
        """

        import hashlib
        import hmac
        import base64

        message = bytes(message, "utf-8")
        secret = bytes(secret, "utf-8")

        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()
        ).decode("utf8")
        return signature

    def get_uuid(self, key1="", key2=""):
        """
        @summary: 计算uuid值
        可用于将两个字符串组成唯一的值。如可将域名和新闻标题组成uuid，形成联合索引
        ---------
        @param key1:str
        @param key2:str
        ---------
        @result:
        """

        uuid_object = ""

        if not key1 and not key2:
            uuid_object = uuid.uuid1()
        else:
            hash = hashlib.md5(bytes(key1, "utf-8") + bytes(key2, "utf-8")).digest()
            uuid_object = uuid.UUID(bytes=hash[:16], version=3)

        return str(uuid_object)

    def get_hash(self, text):
        return hash(text)


x_mm = MM()


# ************************************************ 加密相关模块 --end ************************************************
# ************************************************ 文本相关模块 --start ************************************************

class Text:
    def quote_chinese_word(self, text, encoding="utf-8"):
        def quote_chinese_word_func(text):
            chinese_word = text.group(0)
            return urllib.parse.quote(chinese_word, encoding=encoding)

        return re.sub("([\u4e00-\u9fa5]+)", quote_chinese_word_func, text, flags=re.S)

    def unescape(self, str):
        """
                反转译
                """
        return html.unescape(str)

    def header_to_json(self, text):
        """
        @summary: 可快速将浏览器上的header转为json格式
        ---------
        @param text:
        ---------
        @result:
        """

        contents = text.split("\n")
        json = {}
        for content in contents:
            if content == "\n":
                continue

            content = content.strip()
            regex = ["(:?.*?):(.*)", "(.*?):? +(.*)", "([^:]*)"]

            result = self.get_info(content, regex)
            result = result[0] if isinstance(result[0], tuple) else result
            try:
                json[result[0]] = eval(result[1].strip())
            except:
                json[result[0]] = result[1].strip()

        return json

    def cut_string(self, text, length):
        """
        @summary: 将文本按指定长度拆分
        ---------
        @param text: 文本
        @param length: 拆分长度
        ---------
        @result: 返回按指定长度拆分后形成的list
        """

        text_list = re.findall(".{%d}" % length, text, re.S)
        leave_text = text[len(text_list) * length:]
        if leave_text:
            text_list.append(leave_text)

        return text_list

    def get_random_string(self, length=1):
        random_string = "".join(random.sample(string.ascii_letters + string.digits, length))
        return random_string

    def excape(self, str):
        """
                转译
                """
        return html.escape(str)

    def del_redundant_blank_character(self, text):
        """
        删除冗余的空白符， 只保留一个
        :param text:
        :return:
        """
        return re.sub("\s+", " ", text)

    def is_have_chinese(self, content):
        regex = "[\u4e00-\u9fa5]+"
        chinese_word = self.get_info(content, regex)
        return chinese_word and True or False

    def is_have_english(self, content):
        regex = "[a-zA-Z]+"
        english_words = self.get_info(content, regex)
        return english_words and True or False

    def get_chinese_word(self, content):
        regex = "[\u4e00-\u9fa5]+"
        chinese_word = self.get_info(content, regex)
        return chinese_word

    def get_english_words(self, content):
        regex = "[a-zA-Z]+"
        english_words = self.get_info(content, regex)
        return english_words or ""

    # @log_function_time
    def get_info(self, html, regexs, allow_repeat=True, fetch_one=False, split=None):
        _regexs = {}
        regexs = isinstance(regexs, str) and [regexs] or regexs

        infos = []
        for regex in regexs:
            if regex == "":
                continue

            if regex not in _regexs.keys():
                _regexs[regex] = re.compile(regex, re.S)

            if fetch_one:
                infos = _regexs[regex].search(html)
                if infos:
                    infos = infos.groups()
                else:
                    continue
            else:
                infos = _regexs[regex].findall(str(html))

            if len(infos) > 0:
                # print(regex)
                break

        if fetch_one:
            infos = infos if infos else ("",)
            return infos if len(infos) > 1 else infos[0]
        else:
            infos = allow_repeat and infos or sorted(set(infos), key=infos.index)
            infos = split.join(infos) if split else infos
            return infos

    def table_json(self, table, save_one_blank=True):
        """
                将表格转为json 适应于 key：value 在一行类的表格
                @param table: 使用selector封装后的具有xpath的selector
                @param save_one_blank: 保留一个空白符
                @return:
                """
        data = {}

        trs = table.xpath(".//tr")
        for tr in trs:
            tds = tr.xpath("./td|./th")

            for i in range(0, len(tds), 2):
                if i + 1 > len(tds) - 1:
                    break

                key = tds[i].xpath("string(.)").extract_first(default="").strip()
                value = tds[i + 1].xpath("string(.)").extract_first(default="").strip()
                value = self.replace_str(value, "[\f\n\r\t\v]", "")
                value = self.replace_str(value, " +", " " if save_one_blank else "")

                if key:
                    data[key] = value

        return data

    def replace_str(self, source_str, regex, replace_str=""):
        """
                @summary: 替换字符串
                ---------
                @param source_str: 原字符串
                @param regex: 正则
                @param replace_str: 用什么来替换 默认为''
                ---------
                @result: 返回替换后的字符串
                """
        str_info = re.compile(regex)
        return str_info.sub(replace_str, source_str)

    def get_table_row_data(self, table):
        """
                获取表格里每一行数据
                @param table: 使用selector封装后的具有xpath的selector
                @return: [[],[]..]
                """

        datas = []
        rows = table.xpath(".//tr")
        for row in rows:
            cols = row.xpath("./td|./th")
            row_datas = []
            for col in cols:
                data = col.xpath("string(.)").extract_first(default="").strip()
                row_datas.append(data)
            datas.append(row_datas)

        return datas

    def rows2json(self, rows, keys=None):
        """
                将行数据转为json
                @param rows: 每一行的数据
                @param keys: json的key，空时将rows的第一行作为key
                @return:
                """
        data_start_pos = 0 if keys else 1
        datas = []
        keys = keys or rows[0]
        for values in rows[data_start_pos:]:
            datas.append(dict(zip(keys, values)))

        return datas

    def get_form_data(self, form_text):
        """
                提取form_text中提交的数据
                :param form_text: 使用selector封装后的具有xpath的selector
                :return:
                """
        data = {}
        inputs = form_text.xpath(".//input")
        for input in inputs:
            name = input.xpath("./@name").extract_first()
            value = input.xpath("./@value").extract_first()
            if name:
                data[name] = value

        return data


x_text = Text()


# ************************************************ 文本相关模块 --end ************************************************

# ************************************************ IP相关模块 --start ************************************************
class IP:
    def get_ip(self, domain):
        ip = socket.getaddrinfo(domain, "http")[0][4][0]
        return ip

    def get_localhost_ip(self):
        """
                利用 UDP 协议来实现的，生成一个UDP包，把自己的 IP 放如到 UDP 协议头中，然后从UDP包中获取本机的IP。
                这个方法并不会真实的向外部发包，所以用抓包工具是看不到的
                :return:
                """
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            if s:
                s.close()

        return ip

    def ip_to_num(self, ip):
        import struct

        ip_num = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])
        return ip_num


x_ip = IP()


# ************************************************ IP相关模块 --end ************************************************


# ************************************************ HTML相关模块 --start ************************************************
class HTML:
    def del_html_tag(self, content, except_line_break=False, save_img=False, white_replaced=""):
        """
                删除html标签
                @param content: html内容
                @param except_line_break: 保留p标签
                @param save_img: 保留图片
                @param white_replaced: 空白符替换
                @return:
                """
        content = x_text.replace_str(content, "(?i)<script(.|\n)*?</script>")  # (?)忽略大小写
        content = x_text.replace_str(content, "(?i)<style(.|\n)*?</style>")
        content = x_text.replace_str(content, "<!--(.|\n)*?-->")
        content = x_text.replace_str(
            content, "(?!&[a-z]+=)&[a-z]+;?"
        )  # 干掉&nbsp等无用的字符 但&xxx= 这种表示参数的除外
        if except_line_break:
            content = content.replace("</p>", "/p")
            content = x_text.replace_str(content, "<[^p].*?>")
            content = content.replace("/p", "</p>")
            content = x_text.replace_str(content, "[ \f\r\t\v]")
        elif save_img:
            content = x_text.replace_str(content, "(?!<img.+?>)<.+?>")  # 替换掉除图片外的其他标签
            content = x_text.replace_str(content, "(?! +)\s+", "\n")  # 保留空格
            content = content.strip()
        else:
            content = x_text.replace_str(content, "<(.|\n)*?>")
            content = x_text.replace_str(content, "\s", white_replaced)
            content = content.strip()

        return content

    def del_html_js_css(self, content):
        content = x_text.replace_str(content, "(?i)<script(.|\n)*?</script>")  # (?)忽略大小写
        content = x_text.replace_str(content, "(?i)<style(.|\n)*?</style>")
        content = x_text.replace_str(content, "<!--(.|\n)*?-->")

        return content


x_html = HTML()


# ************************************************ HTML相关模块 --end ************************************************
# ************************************************ Json相关模块 --start ************************************************
class JSON:
    def get_json(self, json_str):
        """
                @summary: 取json对象
                ---------
                @param json_str: json格式的字符串
                ---------
                @result: 返回json对象
                """

        try:
            return json.loads(json_str) if json_str else {}
        except Exception as e1:
            try:
                json_str = json_str.strip()
                json_str = json_str.replace("'", '"')
                keys = x_text.get_info(json_str, "(\w+):")
                for key in keys:
                    json_str = json_str.replace(key, '"%s"' % key)

                return json.loads(json_str) if json_str else {}
            except Exception as e2:
                logging.error(
                    """
                    e1: %s
                    format json_str: %s
                    e2: %s
                    """
                    % (e1, json_str, e2)
                )

            return {}

    def jsonp2json(self, jsonp):
        """
                将jsonp转为json
                @param jsonp: jQuery172013600082560040794_1553230569815({})
                @return:
                """
        try:
            return json.loads(re.match(".*?({.*}).*", jsonp, re.S).group(1))
        except:
            raise ValueError("Invalid Input")

    def dumps_json(self, json_, indent=4, sort_keys=False):
        """
                @summary: 格式化json 用于打印
                ---------
                @param json_: json格式的字符串或json对象
                ---------
                @result: 格式化后的字符串
                """
        try:
            if isinstance(json_, str):
                json_ = self.get_json(json_)

            json_ = json.dumps(
                json_, ensure_ascii=False, indent=indent, skipkeys=True, sort_keys=sort_keys
            )
        except Exception as e:
            logging.error(e)
            json_ = pformat(json_)

        return json_

    def get_json_value(self, json_object, key):
        """
                @summary:
                ---------
                @param json_object: json对象或json格式的字符串
                @param key: 建值 如果在多个层级目录下 可写 key1.key2  如{'key1':{'key2':3}}
                ---------
                @result: 返回对应的值，如果没有，返回''
                """
        current_key = ""
        value = ""
        try:
            json_object = (
                    isinstance(json_object, str) and self.get_json(json_object) or json_object
            )

            current_key = key.split(".")[0]
            value = json_object[current_key]

            key = key[key.find(".") + 1:]
        except Exception as e:
            return value

        if key == current_key:
            return value
        else:
            return self.get_json_value(value, key)

    def get_all_keys(self, datas, depth=None, current_depth=0):
        """
                @summary: 获取json李所有的key
                ---------
                @param datas: dict / list
                @param depth: 字典key的层级 默认不限制层级 层级从1开始
                @param current_depth: 字典key的当前层级 不用传参
                ---------
                @result: 返回json所有的key
                """

        keys = []
        if depth and current_depth >= depth:
            return keys

        if isinstance(datas, list):
            for data in datas:
                keys.extend(self.get_all_keys(data, depth, current_depth=current_depth + 1))
        elif isinstance(datas, dict):
            for key, value in datas.items():
                keys.append(key)
                if isinstance(value, dict):
                    keys.extend(self.get_all_keys(value, depth, current_depth=current_depth + 1))

        return keys

    def to_chinese(self, unicode_str):
        format_str = json.loads('{"chinese":"%s"}' % unicode_str)
        return format_str["chinese"]


x_json = JSON()
# ************************************************ Json相关模块 --end ************************************************
