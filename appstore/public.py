# -*- coding:utf8 -*-
import time
import pymysql


class Public():

    def __init__(self):
        self.base_url = "http://xxx.com"
        self.login_url = self.base_url + "/app/#/home/login"
        self.username = ""
        self.password = ""
        self.mysql_user = ""
        self.mysql_password = ""
        self.mysql_host = ""

    def login_success(self, driver):
        driver.get(self.login_url)
        time.sleep(2)
        driver.find_element_by_id("username").send_keys(self.username)
        driver.find_element_by_id("password").send_keys(self.password)
        driver.find_element_by_xpath(
            "//button[@ng-click='login()']").click()
        time.sleep(2)

    def search_from_mysql(self, database_name, search_sql):
        try:
            conn = pymysql.connect(host=self.mysql_host, port=3306, user=self.mysql_user,
                                   passwd=self.mysql_password, db=database_name, charset='utf8')
            curor = conn.cursor()
            curor.execute(search_sql)
            result = curor.fetchall()
            curor.close()
            conn.close()
            return result
        except Exception as ex:
            return str(ex)


