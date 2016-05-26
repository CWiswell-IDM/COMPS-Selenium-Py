import logging
import unittest
import comps_page_tests
import comps_selenium_pages
import time
from selenium import webdriver

class TestLoginPage(comps_page_tests.CompsPageTest):
    def test_login_testuser(self):
        signin = self.launch_page()
        gooduser = self.config.get_testuser()
        goodpass = self.config.get_testpassword()
        signin.sign_in_as(gooduser, goodpass)
        dash = comps_selenium_pages.DashboardPage(self.driver)
        time.sleep(2) #I'M NOT PROUD OF THIS
        self.assertEqual("COMPS: Dashboard", self.driver.title)

    def test_login_failpassword(self):
        signin = self.launch_page()
        gooduser = self.config.get_testuser()
        badpass = self.config.get_badpassword()
        signin.sign_in_as(gooduser, badpass)
        time.sleep(10) #Not proud, but there is a 5 sec delay built in
        self.assertEqual("COMPS", self.driver.title)
        #Add a check for the error bubble?

    def launch_page(self):
        self.launch_whatever(self.curr_browser)
        self.driver.get(self.config.get_baseurl())
        signin = comps_selenium_pages.SignInPage(self.driver)
        return signin