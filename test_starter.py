import unittest
import comps_selenium_pages
from selenium import webdriver
import time, datetime
import ConfigParser
import logging
import xmlrunner


class TestUIStructure(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("comps_selenium.ini")
        loglevel_string = self.config.get('ACTIVE', 'loglevel')
        loglevel_enum = None
        if loglevel_string == "DEBUG":
            loglevel_enum = logging.DEBUG
        elif loglevel_string == "INFO":
            loglevel_enum = logging.INFO
        elif loglevel_string == "WARNING":
            loglevel_enum = logging.ERROR
        elif loglevel_string == "ERROR":
            loglevel_enum = logging.ERROR
        else:
            raise ValueError("Found loglevel of {v}. Please use DEBUG INFO WARNING or ERROR".format(v=loglevel_string))
        rawdate = datetime.datetime.now()
        tempdate = str(rawdate)
        badchars = [' ', ':', '.']
        for char in badchars:
            tempdate = tempdate.replace(char, '-')
        logname = "log_compsui_{date}.log".format(date=tempdate)
        logging.basicConfig(filename=logname,
                            level=loglevel_enum,
                            format='%(asctime)s: %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S')
        logging.info("{n} beginning".format(n=unittest.TestCase.id(self)))
        env = self.config.get('ACTIVE', 'environment').upper()
        self.browser = self.config.get('ACTIVE', 'browser').lower()
        self.base_url = self.config.get(env, 'base_url')
        self.test_username = self.config.get(env, 'test_username')
        self.test_password = self.config.get(env, 'test_password')
        self.live_username = self.config.get(env, 'live_username')
        self.live_password = self.config.get(env, 'live_password')
        self.bad_password = self.config.get(env, 'bad_password')

    def launch_page(self):
        if self.browser == "chrome":
            self.driver = webdriver.Chrome()
        elif self.browser == "firefox":
            self.driver = webdriver.Firefox()
        else:
            self.assertTrue(False, "ERROR: Please use chrome or firefox as your browser. Check comps_selenium.ini")
        self.driver.implicitly_wait(5)
        self.driver.get(self.base_url)
        signin_page = comps_selenium_pages.SignInPage(self.driver)
        return signin_page

    def launch_dashboard(self):
        signin = self.launch_page()
        signin.sign_in_as(self.test_username, self.test_password)
        dashboard = comps_selenium_pages.DashboardPage(self.driver)
        return dashboard

    def test_page_load(self):
        self.launch_page()
        self.assertEqual("COMPS", self.driver.title)

    @unittest.skip("Don't need this one")
    def test_find_login_form(self):
        self.launch_page()
        login_form_element = self.driver.find_element_by_id("signin")
        # login_form = signin_page.get_signin_form(self.driver)
        size = login_form_element.size
        self.assertEqual(301, size['width'], "Width should be 301")
        self.assertEqual(435, size['height'], "Form should be 435 high")

    @unittest.skip("Don't need this one")
    def test_login_page_username(self):
        signin_page = self.launch_page()
        form = signin_page.get_signin_form(self.driver)
        form.set_name("Slightly stoopid")
        time.sleep(2)
        name_box = self.driver.find_element_by_name("username")
        self.assertEqual("Slightly stoopid", name_box.get_attribute('value'))

    #@unittest.skip("Don't need this one")
    def test_login_liveuser(self):
        signin_page = self.launch_page()
        signin_page.sign_in_as(self.live_username, self.live_password)
        time.sleep(2)
        self.assertEqual("COMPS: Dashboard", self.driver.title)

    def test_login_testuser(self):
        signin = self.launch_page()
        signin.sign_in_as(self.test_username, self.test_password)
        dashboard = comps_selenium_pages.DashboardPage(self.driver)
        self.assertEqual(dashboard.expected_title, self.driver.title)

    def test_login_badpassword(self):
        signin = self.launch_page()
        body = self.driver.find_element_by_tag_name("body")
        bodyclass = body.get_attribute("class")
        logging.info("Bodyclass before login: " + str(bodyclass))
        signin.sign_in_as(self.test_username, self.bad_password)
        body = self.driver.find_element_by_tag_name("body")
        bodyclass = body.get_attribute("class")
        logging.info("Body class after bad: " + str(bodyclass))
        time.sleep(5)
        signin.sign_in_as(self.test_username, self.test_password)
        bodyclass = body.get_attribute("class")
        logging.info("Body class after good: " + str(bodyclass))

    def test_nav_around(self):
        dashboard = self.launch_dashboard()
        sims = dashboard.go_explore_simulations_page()
        self.assertEqual(sims.expected_title, self.driver.title)
        exps = sims.go_explore_experiments_page()
        sims = None
        self.assertEqual(exps.expected_title, self.driver.title)
        stes = exps.go_explore_suites_page()
        exps = None
        self.assertEqual(stes.expected_title, self.driver.title)
        stes.choose_entity("Simulations")
        stes = None
        sims = comps_selenium_pages.SimPage(self.driver)
        self.assertEqual(sims.expected_title, self.driver.title)
        sims.sort_by("DateCreated")
        sims.sort_by("Owner")
        sims.choose_entity("Experiments")
        exps = comps_selenium_pages.ExpPage(self.driver)
        sims = None
        exps.sort_by("DateCreated")
        exps.sort_by("Owner")
        exps.refresh_list()
        self.assertEqual(exps.expected_title, self.driver.title)
        exps.choose_entity("Suites")
        stes = comps_selenium_pages.StePage(self.driver)
        exps = None
        stes.sort_by("DateCreated")
        stes.sort_by("Owner")
        stes.refresh_list()
        self.assertEqual(stes.expected_title, self.driver.title)

    def test_sim_sorting(self):
        dashboard = self.launch_dashboard()
        sims = dashboard.go_explore_simulations_page()
        sims.refresh_table_rows()
        self.assertTrue(sims.check_sort_order("DateCreated", "desc"), msg="Should start as date created descending")
        sims.sort_by("DateCreated")
        self.assertTrue(sims.check_sort_order("DateCreated", "asc"), msg="Should be date created ascending")
        sims.sort_by("Name")
        self.assertTrue(sims.check_sort_order("Name", "desc"), msg="Should be by Name descending")

    def test_switch_environments(self):
        dashboard = self.launch_dashboard()
        dashboard.switch_environment("Metroville")
        active = dashboard.get_active_environment()
        self.assertEqual(active, "Metroville", msg="We should now be in Metroville")
        dashboard.switch_environment("Bayesian")
        active = dashboard.get_active_environment()
        self.assertEqual(active, "Bayesian", msg="We should now be in Bayesian")

    def test_relations(self):
        dash = self.launch_dashboard()
        sims = dash.go_explore_simulations_page()
        self.assertFalse(sims.is_something_selected(), "Nothing should be selected")
        print "NOT DONE HERE"
        self.assertTrue(False, "This isn't done yet")

    def tearDown(self):
        logging.info("tearing down testcase")
        self.driver.close()
        self.driver.quit()

    def test_detail_view(self):
        dashboard = self.launch_dashboard()
        sims = dashboard.go_explore_simulations_page()
        self.assertFalse(sims.is_something_selected(), "Nothing should be selected at first")
        sims.open_detail_view()
        time.sleep(2)
        sims.close_detail_view()
        time.sleep(2)
        sims.toggle_row_by_index(0)
        self.assertTrue(sims.is_something_selected(), "Now something should be selected")
        sims.select_detail("meta")
        time.sleep(2)
        sims.select_detail("spatial")
        time.sleep(2)
        sims.toggle_row_by_index(0)
        self.assertFalse(sims.is_something_selected(), "Now nothing should be selected")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUIStructure)
    xmlrunner.XMLTestRunner("test-reports").run(suite)
    # unittest.main(testRunner=xmlrunner.XMLTestRunner("test-reports"))
