import pymysql
import datetime

from hudongyi_sh_code.settings import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DBNAME,
    MYSQL_TABLE,
)

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DBNAME,
    charset="utf8",
)

cursor = conn.cursor()

"""
    做数据库数据清洗操作
"""


def select_data():
    try:
        dt = (
            "2018-05-30 0:0:00"
        )  # datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        today = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        print(today)
        sql = "SELECT questionId,stockCode,questionTime,replyTime FROM {0} ORDER BY replyTime DESC limit 1000 ".format(
            MYSQL_TABLE
        )
        cursor.execute(sql)
        i = 0
        for info in cursor.fetchall():
            i = i + 1
            info = info
            questionId = info[0]
            questionTime = info[2]
            replyTime = info[3]
            if replyTime > today:
                if replyTime == questionTime:
                    print(questionId)
                    print(
                        "回复时间为：{0}，提问时间{1}，时间大于现在,第{2}条数据".format(
                            replyTime, questionTime, i
                        )
                    )
                    delete_ip(questionId)
            else:
                print("回复时间为：{0}，{1}时间没有大于当前".format(replyTime, questionId))

    except pymysql.Error as e:
        print(e)


def delete_ip(questionId):
    delete_sql = "delete from {0} where questionId='{1}'".format(
        MYSQL_TABLE, questionId
    )
    cursor.execute(delete_sql)
    conn.commit()
    print("{0}删除完毕".format(questionId))
    print("**************************************")


if __name__ == "__main__":
    select_data()
