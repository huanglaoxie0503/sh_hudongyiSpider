import requests
from scrapy.selector import Selector
import pymysql

from hudongyi_sh_code.settings import MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DBNAME

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DBNAME,
    charset="utf8",
)
cursor = conn.cursor()

"""
    维护ip代理池
"""


def crawl_ips():
    headers = {
        "Referer": "http://www.xicidaili.com/nn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    }
    for i in range(1568):
        url = "http://www.xicidaili.com/nn/{0}".format(i)
        response = requests.get(url, headers=headers)
        selector = Selector(text=response.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                """insert into proxy_ip(ip, port, speed, proxy_type)
                          VALUES ('{0}','{1}',{2},'HTTP')
                          ON DUPLICATE KEY UPDATE ip=VALUES (ip),port=VALUES (port),speed=VALUES (speed),proxy_type=VALUES (proxy_type)""".format(
                    ip_info[0], ip_info[1], ip_info[3]
                )
            )
            conn.commit()


class GetIP(object):
    # 删除无效ip
    def delete_ip(self, ip):
        delete_sql = "delete from proxy_ip where ip='{0}'".format(ip)
        # print("无效ip,删除:{0}".format(ip))
        cursor.execute(delete_sql)
        conn.commit()
        return True

    # 判断ip是否有效
    def judge_ip(self, ip, port):
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {"http": proxy_url, "https": proxy_url}
            print("验证中......")
            response = requests.get(http_url, proxies=proxy_dict)
            print("验证完毕......")
            return True
        except Exception as e:
            print("经检验是invalid ip")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip and port")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库随机取一个ip
        random_sql = "select ip,port from proxy_ip ORDER BY RAND() limit 1"
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    # crawl_ips()
    get_ip = GetIP()
    ip = get_ip.get_random_ip()
    print(ip)
