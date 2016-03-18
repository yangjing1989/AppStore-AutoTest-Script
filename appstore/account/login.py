# -*- coding:utf8  -*-
import time
import unittest

import HTMLTestRunner
from selenium import webdriver

import url_test


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "http://xxx.com"
        self.login_url = self.base_url + "/app/#/home/login"
        self.welcome_url = self.base_url + "/app/#/home/welcome"
        self.empty_text = "用户名或密码不能为空!"
        self.error_text = "用户名或者密码错误，请重试"
        self.username = ""
        self.password = ""

    def test_url_reachable(self):
        response_code = url_test.UrlTest(self.login_url)
        self.assertTrue(response_code)

    def test_empty_all(self):
        self.page_element_operation("", "")
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.empty_text)
        alert_win.accept

    def test_empty_user(self):
        self.page_element_operation("", self.password)
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.empty_text)
        alert_win.accept

    def test_empty_password(self):
        self.page_element_operation(self.username, "")
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.empty_text)
        alert_win.accept

    def test_error_password(self):
        self.page_element_operation(self.username, "111111")
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.error_text)
        alert_win.accept

    def test_right_password(self):
        self.page_element_operation(self.username, self.password)
        time.sleep(2)
        cur_url = self.driver.current_url
        self.assertEqual(cur_url, self.welcome_url)

    def page_element_operation(self, username, password):
        self.driver.get(self.login_url)
        time.sleep(2)
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_xpath(
            "//button[@ng-click='login()']").click()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(LoginTest("test_url_reachable"))
    test_suite.addTest(LoginTest("test_empty_all"))
    test_suite.addTest(LoginTest("test_empty_user"))
    test_suite.addTest(LoginTest("test_empty_password"))
    test_suite.addTest(LoginTest("test_error_password"))
    test_suite.addTest(LoginTest("test_right_password"))
    report_file = "/yangjing/appstore/report/login.html"
    fp = open(report_file, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp, title='login_report',
        description='')
    runner.run(test_suite)
