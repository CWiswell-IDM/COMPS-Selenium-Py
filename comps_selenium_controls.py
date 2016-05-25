from selenium import webdriver

class CompsControl:
    def __init__(self, driver):
        self.myElement = None
        self.driver = driver
        
    def findMe(self, driver):
        if self.finderType == "by_name":
            self.myElement = driver.find_element_by_name(self.finderValue)
        elif self.finderType == "by_css_selector":
            self.myElement = driver.find_element_by_css_selector(self.finderValue)
        elif self.finderType == "by_link_text":
            self.myElement = driver.find_element_by_link_text(self.finderValue)
        elif self.finderType == "by_id":
            self.myElement = driver.find_element_by_id(self.finderValue)

class CompsTextbox(CompsControl):
    def __init__(self, driver, finder_value):
        self.finderType = "by_name"
        self.finderValue = finder_value

    def set_text(self, chosen_text):
        self.myElement.clear()
        self.myElement.send_keys(chosen_text)
        
    def get_text(self):
        return self.myElement.get_attribute("value")

class CompsButton(CompsControl):
    def __init__(self, driver, finder_value):
        self.finderType = "by_css_selector"
        self.finderValue = finder_value
        
    def click(self):
        self.myElement.click()

class SignInForm(CompsControl):
    def __init__(self, driver):
        self.driver = driver
        self.finderType = "by_id"
        self.finderValue = "signin"
        self.name_box = None
        self.pass_box = None
        self.click_button = None
        self.forgot_link = None
        self.note_toggle = None
        
    def set_name(self, chosen_name):
        if not self.name_box:
            self.name_box = CompsTextbox(self.driver, "username")
            self.name_box.findMe(self.driver)
        self.name_box.set_text(chosen_name)
        
    def set_password(self, chosen_password):
        if not self.pass_box:
            self.pass_box = CompsTextbox(self.driver, "password")
            self.pass_box.findMe(self.driver)
        self.pass_box.set_text(chosen_password)
        
    def submit_form(self):
        if not self.click_button:
            self.click_button = CompsButton(self.driver, "input[value='Sign In']")
            self.click_button.findMe(self.driver)
        self.click_button.click()
    
    def toggle_note(self):
        pass
        
    def is_note_visible(self):
        pass