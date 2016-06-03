import logging
import unittest
import comps_test_config
import datetime

class CompsPageTest(unittest.TestCase):
    def setUp(self):
        #Read config
        self.config = comps_test_config.CompsTestConfig()

        #Determine starttime
        starttime = datetime.datetime.now()
        startstring = str(starttime)
        badchars = [' ', ':', '.']
        for badchar in badchars:
            startstring = startstring.replace(badchar, '-')

        #Set up logging
        if self.config.is_logging():
            loglevel_string = self.config.get_loglevel()
            loglevel = self.get_log_level(loglevel_string)

            logname = self.config.get_logname().format(date=startstring)

            logging.basicConfig(filename=logname,
                                level=loglevel,
                                format=self.config.get_logname_format(),
                                datefmt=self.config.get_dateformat())

        #Select browser(s). This is built with the ideo of adding "all" later
        #and having the code loop through the browsers with each test
        #which is why there is that weird "remaining browsers" thing in there
        browser_config = self.config.get_browser()
        self.remaining_browsers = []
        valid_browser_configs = ["chrome","firefox","ie","phantom"]
        if browser_config not in valid_browser_configs:
            raise ValueError(
                msg="Browser {b} not in {v}. Please try one of those.".format(
                b=browser_config,
                v=str(valid_browser_configs)
            ))
        else:
            self.remaining_browsers.append(browser_config)
        self.curr_browser = self.remaining_browsers.pop(0)
        self.driver = None

    def get_log_level(self, log_level_string):
        log_level_string = log_level_string.upper()
        loglevel_enum = None
        if log_level_string == "DEBUG":
            loglevel_enum = logging.DEBUG
        elif log_level_string == "INFO":
            loglevel_enum = logging.INFO
        elif log_level_string == "WARNING":
            loglevel_enum = logging.ERROR
        elif log_level_string == "ERROR":
            loglevel_enum = logging.ERROR
        return  loglevel_enum

    def launch_whatever(self, browser):
        from selenium import webdriver
        if browser == "chrome":
            self.driver = webdriver.Chrome()
        elif browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "ie":
            self.driver = webdriver.Ie()
        elif browser == "phantom":
            self.driver = webdriver.PhantomJS()
        else:
            raise ValueError("{b} isn't going to work".format(b=browser))

    def launch_page(self):
        self.launch_whatever(self.curr_browser)
        self.driver.get(self.config.get_baseurl())

    def tearDown(self):
        if self.driver:
            self.driver.quit()