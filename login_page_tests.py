import logging
import unittest
import comps_page_tests
import comps_selenium_pages
import time
from selenium import webdriver

class TestLoginPage(comps_page_tests.CompsPageTest):
    def test_login_testuser(self):
        self.launch_page()
        signin = comps_selenium_pages.SignInPage(self.driver)
        gooduser = self.config.get_testuser()
        goodpass = self.config.get_testpassword()
        signin.sign_in_as(gooduser, goodpass)
        dash = comps_selenium_pages.DashboardPage(self.driver)
        time.sleep(2) #I'M NOT PROUD OF THIS
        self.assertEqual("COMPS: Dashboard", self.driver.title)

    def test_login_failpassword(self):
        self.launch_page()
        signin = comps_selenium_pages.SignInPage(self.driver)
        gooduser = self.config.get_testuser()
        badpass = self.config.get_badpassword()
        signin.sign_in_as(gooduser, badpass)
        time.sleep(10) #Not proud, but there is a 5 sec delay built in
        self.assertEqual("COMPS", self.driver.title)
        #Add a check for the error bubble?