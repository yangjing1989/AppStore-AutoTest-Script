# -*- coding:utf8 -*-
import HTMLTestRunner
import time
import unittest
import public
from selenium import webdriver


class Search(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "http://xxx.com"
        self.login_url = self.base_url + "/app/#/home/login"
        public.Public().login_success(self.driver)
        self.driver.find_element_by_link_text("应用列表").click()
        time.sleep(5)
        self.name = self.driver.find_element_by_xpath("//input[@ng-model='name']")
        self.package = self.driver.find_element_by_xpath("//input[@ng-model='package']")
        self.developer = self.driver.find_element_by_xpath("//input[@ng-model='developer']")
        self.tag = self.driver.find_element_by_xpath("//input[@ng-model='tag']")
        self.category = self.driver.find_element_by_name("classify")
        self.source = self.driver.find_element_by_xpath("//select[@ng-change='changeSource()']")
        self.status = self.driver.find_element_by_name("status")
        self.search = self.driver.find_element_by_xpath("//button[@ng-click='search()']")
        self.count_text = self.driver.find_element_by_xpath("//span[@class='ng-binding']")
        self.app_database = "xxx_com"

    def test_search_by_name(self):
        self.search_by_name("cc")
        self.search_by_name("运动")
        self.search_by_name("!")
        self.search_by_name("*")
        self.search_by_name("0")

    def test_search_by_package(self):
        self.search_by_package("com.weimeng.mami")
        self.search_by_package("com.com2us.tinypang.momo.freefull.momo.cn.android.common")
        self.search_by_package("CRM.Android.KASS")
        self.search_by_package("*")
        self.search_by_package("0")

    def test_search_by_developer(self):
        self.search_by_developer("百度")
        self.search_by_developer("Smartisan")
        self.search_by_developer("*")
        self.search_by_developer("0")

    def test_search_by_tag(self):
        self.search_by_tag("拼音")
        self.search_by_tag("Google")
        self.search_by_tag("163")
        self.search_by_tag("*")
        self.search_by_tag("0")

    def test_search_by_category(self):
        all_options = self.category.find_elements_by_tag_name("option")
        for option in all_options:
            option.click()
            time.sleep(2)
            actual_search_count = int(self.count_text.text[3:len(self.count_text.text)-1])
            if option.text == "全部":
                search_sql = "select count(*) from app where status!=-1 and status!=4;"
            else:
                search_sql = "select count(*) from app_category_app as aca,app_category as ac, app as a where ac.name ='"\
                             + option.text + "' and aca.c_id=ac.id and aca.app_id=a.id and a.status!=-1 and a.status!=4 ;"
            expect_search_count = public.Public().search_from_mysql(self.app_database, search_sql)
            expect_search_count = int(expect_search_count[0][0])
            self.assertEqual(actual_search_count, expect_search_count)
            time.sleep(2)

    def test_search_by_source(self):
        all_options = self.source.find_elements_by_tag_name("option")
        for option in all_options:
            option.click()
            time.sleep(2)
            actual_search_count = int(self.count_text.text[3:len(self.count_text.text)-1])
            if option.text == "全部":
                search_sql = "select count(*) from app where status!=-1 and status!=4;"
            else:
                if option.text == "本地上传":
                    source_value = 0
                elif option.text == "豌豆荚":
                    source_value = 1
                elif option.text == "应用宝":
                    source_value = 2
                elif option.text == "开发者中心":
                    source_value = 3
                elif option.text == "九游":
                    source_value = 4
                search_sql = "select count(*) from app where source="+str(source_value)+" and status!=-1 and status!=4 ;"
            expect_search_count = public.Public().search_from_mysql(self.app_database, search_sql)
            expect_search_count = int(expect_search_count[0][0])
            self.assertEqual(actual_search_count, expect_search_count)
            time.sleep(2)

    def test_search_by_status(self):
        all_options = self.status.find_elements_by_tag_name("option")
        for option in all_options:
            option.click()
            time.sleep(2)
            actual_search_count = int(self.count_text.text[3:len(self.count_text.text)-1])
            if option.text == "全部":
                search_sql = "select count(*) from app where status!=-1 and status!=4;"
            else:
                if option.text == "待审核":
                    status_value = 2
                elif option.text == "已上架":
                    status_value = 1
                elif option.text == "已下架":
                    status_value = 0
                elif option.text == "拒绝上架":
                    status_value = -2
                elif option.text == "已下架":
                    status_value = 0
                elif option.text == "临时":
                    status_value = 3
                elif option.text == "预发布":
                    status_value = 5
                search_sql = "select count(*) from app where status="+str(status_value)+" and status!=-1 and status!=4 ;"
            expect_search_count = public.Public().search_from_mysql(self.app_database, search_sql)
            expect_search_count = int(expect_search_count[0][0])
            self.assertEqual(actual_search_count, expect_search_count)
            time.sleep(2)

    def search_by_name(self, keyword):
        self.name.send_keys(keyword)
        self.search.click()
        time.sleep(2)
        actual_search_count = int(self.count_text.text[3:len(self.count_text.text)-1])
        search_sql = "select count(*) from app where (name like '%"+\
                     keyword+"%' or cname like '%"+keyword+"%') and status!=-1 and status!=4;"
        expect_search_count = public.Public().search_from_mysql(self.app_database, search_sql)
        expect_search_count = int(expect_search_count[0][0])
        self.assertEqual(actual_search_count, expect_search_count)
        self.name.clear()

    def search_by_package(self, package):
        self.package.send_keys(package)
        self.search.click()
        time.sleep(2)
        actual_search_count = int(self.count_text.text[3:len(self.count_text.text)-1])
        search_sql = "select count(*) from app where package='"+package+"' and status!=-1 and status!=4;"
        expect_search_count = public.Public().search_from_mysql(self.app_database, search_sql)
        expect_search_count = int(expect_search_count[0][0])
        self.assertEqual(actual_search_count, expect_search_count)
        self.package.clear()

    def search_by_developer(self, keyword):
        self.developer.send_keys(keyword)
        self.search.click()
        time.sleep(2)
        actual_search_count = int(self.count_text.text[3:len(self.count_text.text)-1])
        search_sql = "select count(*) from app where developer like'%"+keyword+"%' and status!=-1 and status!=4;"
        expect_search_count = public.Public().search_from_mysql(self.app_database, search_sql)
        expect_search_count = int(expect_search_count[0][0])
        self.assertEqual(actual_search_count, expect_search_count)
        self.developer.clear()

    def search_by_tag(self, keyword):
        self.tag.send_keys(keyword)
        self.search.click()
        time.sleep(2)
        actual_search_count = int(self.count_text.text[3:len(self.count_text.text)-1])
        search_sql = "select count(*) from app,app_tag where app_tag.tag like'%"\
                     +keyword+"%' and app_tag.app_id=app.id and app.status!=-1 and app.status!=4;"
        expect_search_count = public.Public().search_from_mysql(self.app_database, search_sql)
        expect_search_count = int(expect_search_count[0][0])
        self.assertEqual(actual_search_count, expect_search_count)
        self.tag.clear()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(Search("test_search_by_name"))
    test_suite.addTest(Search("test_search_by_package"))
    test_suite.addTest(Search("test_search_by_developer"))
    test_suite.addTest(Search("test_search_by_tag"))
    test_suite.addTest(Search("test_search_by_category"))
    test_suite.addTest(Search("test_search_by_source"))
    test_suite.addTest(Search("test_search_by_status"))
    filename = "/yangjing/appstore/report/search.html"
    fp = open(filename, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="app_search_report")
    runner.run(test_suite)
