# -*- coding:utf8  -*-
import HTMLTestRunner
import time
import unittest

from selenium import webdriver


class ModifyPassword(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "http://xxx.com"
        self.login_url = self.base_url + "/app/#/home/login"
        self.welcome_url = self.base_url + "/app/#/home/welcome"
        self.empty_text = "请填写完整"
        self.error_old_text = "密码错误，请重新输入"
        self.not_same_text = "两次密码不匹配"
        self.less_six_text = "新密码不能小于6位"
        self.right_text = "密码修改成功!"
        self.old_password = "xxx"
        self.new_password = "xxx"

    def test_empty_all(self):
        self.login(self.old_password)
        self.page_element_operation("", "", "")
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.empty_text)

    def test_empty_old(self):
        self.login(self.old_password)
        self.page_element_operation("", self.new_password, self.new_password)
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.empty_text)

    def test_empty_new(self):
        self.login(self.old_password)
        self.page_element_operation(self.old_password, "", "")
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.empty_text)

    def test_not_same(self):
        self.login(self.old_password)
        self.page_element_operation(self.old_password, self.new_password, self.old_password)
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.not_same_text)

    def test_error_old(self):
        self.login(self.old_password)
        self.page_element_operation(self.new_password, self.new_password, self.new_password)
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.error_old_text)

    def test_less_six(self):
        self.login(self.old_password)
        self.page_element_operation(self.old_password, self.new_password[0:4], self.new_password[0:4])
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.less_six_text)

    def test_right_modify(self):
        self.login(self.old_password)
        self.page_element_operation(self.old_password, self.new_password, self.new_password)
        alert_win = self.driver.switch_to.alert
        self.assertEqual(alert_win.text, self.right_text)
        alert_win.accept()
        time.sleep(2)
        self.driver.find_element_by_link_text("欢迎你：xxx").click()
        self.driver.find_element_by_xpath("//a[@ng-click='logout()']").click()
        self.login(self.new_password)
        self.assertEqual(self.driver.current_url, self.welcome_url)
        self.page_element_operation(self.new_password, self.old_password, self.old_password)

    def page_element_operation(self, old, new, renew):
        self.driver.find_element_by_link_text("欢迎你：xxx").click()
        self.driver.find_element_by_xpath("//a[@ng-click='showUpdatePwd()']").click()
        time.sleep(2)
        self.driver.find_element_by_id("oldpasswd").send_keys(old)
        self.driver.find_element_by_id("newpasswd").send_keys(new)
        self.driver.find_element_by_xpath("//input[@ng-model='updatepwd.renewpassword']").send_keys(renew)
        self.driver.find_element_by_xpath("//button[@ng-click='ok()']").click()
        time.sleep(2)

    def login(self, password):
        self.driver.get(self.login_url)
        time.sleep(2)
        self.driver.find_element_by_id("username").send_keys("")
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_xpath(
            "//button[@ng-click='login()']").click()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(ModifyPassword("test_empty_all"))
    test_suite.addTest(ModifyPassword("test_empty_old"))
    test_suite.addTest(ModifyPassword("test_empty_new"))
    test_suite.addTest(ModifyPassword("test_not_same"))
    test_suite.addTest(ModifyPassword("test_error_old"))
    test_suite.addTest(ModifyPassword("test_less_six"))
    test_suite.addTest(ModifyPassword("test_right_modify"))
    report_file = "/yangjing/appstore/report/modify_password.html"
    fp = open(report_file, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="modify_password_report")
    runner.run(test_suite)
