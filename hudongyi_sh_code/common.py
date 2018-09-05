#!/usr/bin/env python3
import datetime
import re
import pymysql
from hudongyi_sh_code.settings import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DBNAME,
    MYSQL_TABLE,
    mysql_uid_table,
)

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DBNAME,
    charset="utf8",
)
cursor = conn.cursor()


def question_datetime_parse(quetionTime):
    try:
        if "小时前" in quetionTime:
            temp = quetionTime.replace("小时前", "")
            quetionTime = (
                datetime.datetime.now() - datetime.timedelta(hours=int(temp))
            ).strftime("%Y-%m-%d %H:%M:%S")
            return quetionTime
        elif "分钟前" in quetionTime:
            temp = quetionTime.replace("分钟前", "")
            quetionTime = (
                datetime.datetime.now() - datetime.timedelta(minutes=int(temp))
            ).strftime("%Y-%m-%d %H:%M:%S")
            return quetionTime
        elif "秒前" in quetionTime:
            temp = quetionTime.replace("秒前", "")
            quetionTime = (
                datetime.datetime.now() - datetime.timedelta(seconds=int(temp))
            ).strftime("%Y-%m-%d %H:%M:%S")
            return quetionTime
        elif "昨天" in quetionTime:
            temp = quetionTime.replace("昨天", "")
            quetionTime = (
                (datetime.date.today() - datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                )
                + temp
                + ":00"
            )
            return quetionTime
        else:
            quetion_month = quetionTime.split("-")[0]
            cur_month = datetime.date.today().month
            if int(quetion_month) > cur_month:
                year = datetime.date.today().year - 1
                quetionTime = str(year) + "-" + quetionTime + ":00"
                return quetionTime
            else:
                year = datetime.date.today().strftime("%Y")
                quetionTime = year + "-" + quetionTime + ":00"
                return quetionTime
    except Exception as e:
        print(e)


def reply_datetime_parse(replyTime):
    try:
        if "小时前" in replyTime:
            temp = replyTime.replace("小时前", "")
            replyTime = (
                datetime.datetime.now() - datetime.timedelta(hours=int(temp))
            ).strftime("%Y-%m-%d %H:%M:%S")
            return replyTime
        elif "分钟前" in replyTime:
            temp = replyTime.replace("分钟前", "")
            replyTime = (
                datetime.datetime.now() - datetime.timedelta(minutes=int(temp))
            ).strftime("%Y-%m-%d %H:%M:%S")
            return replyTime
        elif "秒前" in replyTime:
            temp = replyTime.replace("秒前", "")
            replyTime = (
                datetime.datetime.now() - datetime.timedelta(seconds=int(temp))
            ).strftime("%Y-%m-%d %H:%M:%S")
            return replyTime
        elif "昨天" in replyTime:
            temp = replyTime.replace("昨天", "")
            replyTime = (
                (datetime.date.today() - datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                )
                + temp
                + ":00"
            )
            return replyTime
        else:
            year = datetime.date.today().strftime("%Y")
            replyTime = year + "-" + replyTime + ":00"
            return replyTime
    except Exception as e:
        print(e)


def get_url_uid():
    try:
        uid_list = []
        sql = """SELECT url FROM {0};""".format(mysql_uid_table)
        cursor.execute(sql)
        recodes = cursor.fetchall()
        for line in recodes:
            line = line[0].replace("\n", "")
            line = re.findall(r"(\d+)", line)
            uid_list.append(line[0])
        return uid_list
    except Exception as e:
        print(e)


def get_max_time(code):
    """
        按公司代码从数据库获取做大时间并返回
    :param code:
    :return:
    """
    try:
        sql = "select max(replyTime) from {0} WHERE stockCode={1}".format(
            MYSQL_TABLE, code
        )
        cursor.execute(sql)
        max_time = cursor.fetchall()[0][0]
        return max_time
    except pymysql.Error as e:
        print(e)


def get_question_id(art_id):
    """验证question_id数据库是否已经存在"""
    try:
        sql = "select * from {0} where questionId=%s;".format(MYSQL_TABLE)
        cursor.execute(sql, (art_id,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except pymysql.Error as e:
        print(e)


if __name__ == "__main__":
    get_max_time("600000")
