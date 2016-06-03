import unittest
import comps_page_tests
import comps_selenium_pages
import time

class TestGridPage(comps_page_tests.CompsPageTest):
    def test_starting_page_length(self):
        sims = self.log_into_sims_page()

        #Get into simulations page
        #Make sure that there are enough sims
        #Check start page length

    def log_into_sims_page(self):
        self.launch_page()
        signin = comps_selenium_pages.SignInPage(self.driver)
        test_user = self.config.get_testuser()
        test_pass = self.config.get_testpassword()
        signin.sign_in_as(test_user, test_pass)
        dash = comps_selenium_pages.DashboardPage(self.driver)
        sims = dash.go_explore_simulations_page()
        return sims


