import comps_page_tests

class FrameworkUnittest(comps_page_tests.CompsPageTest):
    def test_logging_works(self):
        import logging
        logging.info(msg="Info message!")
        logging.debug(msg="Debug message!")
        logging.warn(msg="warning message!")
        logging.error(msg="Oh carp, error message!")

    def test_chrome_launches(self):
        self.launch_whatever("chrome")

    def test_firefox_launches(self):
        self.launch_whatever("firefox")

    def test_ie_launches(self):
        self.launch_whatever("ie")

    def test_phantom_launches(self):
        self.launch_whatever("phantom")
