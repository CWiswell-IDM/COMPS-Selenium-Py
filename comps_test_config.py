import ConfigParser

class CompsTestConfig():
    def __init__(self, config_file_name="comps_selenium.ini"):
        self.config = ConfigParser.ConfigParser()
        self.config.read("comps_selenium.ini")
        self.env = self.config.get('ACTIVE', 'environment').upper()

    def is_logging(self):
        return self.config.getboolean('LOG', 'do_logging')

    def get_logname(self):
        return self.config.get('LOG', 'logname')

    def get_loglevel(self):
        return self.config.get('LOG', 'loglevel')

    def get_dateformat(self):
        return self.config.get('LOG', 'dateformat')

    def get_logname_format(self):
        return("%(asctime)s: %(levelname)s: %(message)s")
        #I couldn't figure out how to read this out of
        #an .ini file. I could probably do it with .json
        #but that isn't important right now.
        #return self.config.get('LOG', 'lognameformat')

    def get_browser(self):
        return self.config.get('ACTIVE', 'browser')

    def get_baseurl(self):
        return self.config.get(self.env, 'base_url')

    def get_testuser(self):
        return self.config.get(self.env, 'test_username')

    def get_testpassword(self):
        return self.config.get(self.env, 'test_password')

    def get_badpassword(self):
        return self.config.get(self.env, 'bad_password')


