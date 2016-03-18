# -*- coding:utf8  -*-
import HTMLTestRunner
import time
import unittest

from selenium import webdriver


class Logout(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "http://xxx.com"
        self.login_url = self.base_url + "/app/#/home/login"
        self.driver.get(self.login_url)
        time.sleep(2)
        self.driver.find_element_by_id("username").send_keys("")
        self.driver.find_element_by_id("password").send_keys("")
        self.driver.find_element_by_xpath(
            "//button[@ng-click='login()']").click()
        time.sleep(2)

    def test_logout(self):
        login_cookies_list = self.get_cur_cookies()
        self.assertTrue("userInfo" in login_cookies_list)
        self.assertTrue("isLogin" in login_cookies_list)
        self.assertTrue(login_cookies_list["isLogin"])
        self.driver.find_element_by_link_text("欢迎你：superadmin").click()
        self.driver.find_element_by_xpath("//a[@ng-click='logout()']").click()
        time.sleep(2)
        logout_cookies_list = self.get_cur_cookies()
        self.assertFalse("userInfo" in logout_cookies_list)
        self.assertFalse("isLogin" in logout_cookies_list)

    def get_cur_cookies(self):
        cookies_list = self.driver.get_cookies()
        cookie_dict = {}
        for cookies in cookies_list:
            cookie_key = cookies.get("name")
            cookie_value = cookies.get("value")
            cookie_dict[cookie_key] = cookie_value
        return cookie_dict

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(Logout("test_logout"))
    filename = "/yangjing/appstore/report/logout.html"
    fp = open(filename, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="logout_report")
    runner.run(test_suite)
