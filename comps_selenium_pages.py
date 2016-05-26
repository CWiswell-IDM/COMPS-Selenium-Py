from selenium import webdriver
import datetime
import time
import comps_selenium_controls
import logging

class SignInPage:
    
    def __init__(self, driver):
        self.driver = driver
        self.signin_form_id = "signin"
        self.signin_form = None
        page_title = None
        while not page_title:
            time.sleep(1)
            page_title = driver.title
        max_wait_time = datetime.timedelta(seconds=10)
        ready = False
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while (not ready) and ((curr_time - start_time) < max_wait_time):
            bodies = self.driver.find_elements_by_tag_name("BODY")
            if len(bodies) > 0:
                bodyclass = bodies[0].get_attribute("class")
                if "unready" not in bodyclass and "ready" in bodyclass:
                    ready = True
            time.sleep(0.2)
            curr_time = datetime.datetime.now()
        
    def get_signin_form(self, driver):
        if not self.signin_form:
            self.signin_form = comps_selenium_controls.SignInForm(driver)
            self.signin_form.findMe(driver)
        return self.signin_form
        
    def sign_in_as(self, username, password):
        form = self.get_signin_form(self.driver)
        form.set_name(username)
        form.set_password(password)
        form.submit_form()

class CompsPage(object):
    def __init__(self, driver, title):
        self.expected_title = title
        self.driver = driver
        self.tribar_id = "tribar"
        self.tribar = None
        ready = False
        bodyclass = ""
        max_wait_time = datetime.timedelta(seconds=10)
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while (not ready) and (not self.tribar) and ((curr_time - start_time) < max_wait_time):
            bodies = self.driver.find_elements_by_tag_name("BODY")
            if len(bodies) > 0:
                bodyclass = bodies[0].get_attribute("class")
                if "unready" not in bodyclass and "ready" in bodyclass:
                    ready = True
            if not self.tribar:
                tribars = self.driver.find_elements_by_id(self.tribar_id)
                if len(tribars) > 0:
                    self.tribar = tribars[0]
            time.sleep(0.2)
            curr_time = datetime.datetime.now()
        self.load_time = curr_time - start_time
        logging.info("Page: {n} loaded in {t}".format(n=self.__class__.__name__,t=str(self.load_time)))

    def show_tribar_menu(self):
        if not self.tribar_menu_displayed:
            self.tribar.click()
        else:
            return
        
    @property
    def tribar_menu_displayed(self):
        if not self.tribar:
            self.tribar = self.driver.find_element_by_id(self.tribar_id)
        dropdowns = self.tribar.find_elements_by_tag_name("menu")
        if len(dropdowns) > 0:
            return True
        else:
            return False

    def switch_environment(self, env_name):
        header = self.driver.find_element_by_id("header")
        spans = header.find_elements_by_css_selector("span")
        foundIt = False
        for span in spans:
            if span.get_attribute("title") == "Environments":
                span.click()
                foundIt = True
                break
            if not foundIt:
             raise ValueError("No span with title 'Environments' found.")
        header.find_element_by_link_text(env_name).click()

    def get_active_environment(self):
        header = self.driver.find_element_by_id("header")
        menus = header.find_elements_by_tag_name("menu")
        envs_menu = None
        for menu in menus:
            if menu.get_attibute("class") == "dropdown":
                envs_menu = menu
                break
        if not envs_menu:
            raise ValueError("Couldn't find a menu with class 'dropdown'")
        lis = envs_menu.find_elements_by_tag_name("li")
        for li in lis:
            if li.get_attribute("class") == "active":
                return

    def go_dashboard_page(self):
        pass
        
    def go_explore_page(self):
        pass
        
    def go_explore_simulations_page(self):
        url = self.driver.current_url
        base = url.split('#')[0]
        explore_sims_suffix = "explore/Simulations"
        default_sort = "orderby=DateCreated+desc&count=10&offset=0"
        sims_url = "{0}#{1}?{2}".format(base, explore_sims_suffix, default_sort)
        self.driver.get(sims_url)
        #self.show_tribar_menu()
        #explore = self.driver.find_elements_by_link_text("Explore")
        #explore[0].click()
        return SimPage(self.driver)
        
    def go_explore_experiments_page(self):
        url = self.driver.current_url
        base = url.split('#')[0]
        explore_exps_suffix = "explore/Experiments"
        default_sort = "orderby=DateCreated+desc&count=10&offset=0"
        exp_url = "{0}#{1}?{2}".format(base, explore_exps_suffix, default_sort)
        self.driver.get(exp_url)
        return ExpPage(self.driver)
        
    def go_explore_suites_page(self):
        url = self.driver.current_url
        base = url.split('#')[0]
        explore_suites_suffix = "explore/Suites"
        default_sort = "orderby=DateCreated+desc&count=10&offset=0"
        suites_url = "{0}#{1}?{2}".format(base, explore_suites_suffix, default_sort)
        self.driver.get(suites_url)
        return StePage(self.driver)
        
    def go_explore_workitems_page(self):
        pass
        
    def go_create_page(self):
        pass
        
    def go_create_input_page(self):
        pass
        
    def go_create_workitem_page(self):
        pass
        
    def go_create_simulation_page(self):
        pass
        
    def go_about_page(self):
        pass
        
    def go_about_software_page(self):
        pass
        
    def go_about_component_page(self):
        pass
        
    def go_about_code_page(self):
        pass
       
    def go_administer_page(self):
        pass
       
    def go_administer_password_page(self):
        pass

    def sign_out_tribar(self):
        if not self.tribar_menu_displayed():
            self.show_tribar_menu()
            sign_out = self.driver.find_element_by_link_text("Sign-Out")
            sign_out.click()
        pass

class GridPage(CompsPage):
    def __init__(self, driver, title):
        super(GridPage, self).__init__(driver, title)
        self.grid = self.driver.find_element_by_class_name("grid")
        self.t_head = self.driver.find_element_by_tag_name("thead")
        self.t_body = self.driver.find_element_by_tag_name("tbody")
        self.sorters = None
        self.rows = None
        self.sorters = {}
        self.alpha_sort_fields = ["Owner","Name","Description"]
        self.time_sort_fields = ["DateCreated","DateModified"]
        self.valid_detail_tabs = ["meta", "config"]
        self.valid_sort_fields = self.alpha_sort_fields + self.time_sort_fields
        sorter_list = self.t_head.find_elements_by_tag_name("th")
        for sorter in sorter_list:
            data_item = sorter.get_attribute("data-item")
            self.sorters[data_item] = sorter

    def add_clause(self, clause_type, clause_value, clause_operator='equals'):
        raise NotImplementedError()

    def choose_entity(self, entity_type):
        if entity_type not in ["Simulations","Experiments","Suites","Workitems"]:
            raise ValueError("Please use 'Simulations' 'Experiments' 'Suites' 'Workitems'")
        entity_field = self.driver.find_element_by_class_name("entity")
        entity_field.click()
        link = self.driver.find_element_by_link_text(entity_type)
        link.click()

    def sort_by(self, sorter):
        self.sorters[sorter].click()
        self.wait_for_ready()
        self.refresh_table_rows()

    def refresh_list(self):
        self.driver.find_element_by_name("refresh").click()
        self.wait_for_ready()
        self.refresh_table_rows()

    def wait_for_ready(self, max_wait_in_seconds=10):
        ready = False
        bodyclass = ""
        max_wait_time = datetime.timedelta(seconds=max_wait_in_seconds)
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        while (not ready) and (curr_time - start_time < max_wait_time):
            bodies = self.driver.find_elements_by_tag_name("BODY")
            if len(bodies) > 0:
                bodyclass = bodies[0].get_attribute("class")
                if "fetching" not in bodyclass and "ready" in bodyclass:
                    ready = True
            time.sleep(0.2)
            curr_time = datetime.datetime.now()

    def refresh_table_rows(self):
        self.rows = []
        self.t_body = self.driver.find_element_by_tag_name("tbody")
        rows = self.t_body.find_elements_by_tag_name("tr")
        for row in rows:
            if row.is_displayed():
                self.rows.append(row)

    def sort_value_for_row(self, row, sort_field):
        """Only works for time right now, alpha methods aren't working"""
        tds = row.find_elements_by_tag_name("td")
        if sort_field in ["Name","Description"]:
            itemprop = "Meta"
        else:
            itemprop = sort_field
        for td in tds:
            if itemprop == td.get_attribute("itemprop"):
                if itemprop in self.time_sort_fields:
                    rawtime = td.find_element_by_tag_name("time").get_attribute("datetime")
                    dt = datetime.datetime.strptime(rawtime, "%Y-%m-%dT%H:%M:%S.%f0Z")
                    return dt
                elif itemprop == "Owner":
                    return td.text
                else: #field is in itemprop="Meta"
                    if sort_field == "Name":
                        dts = td.find_elements_by_tag_name("dt")
                        for dt in dts:
                            if dt.get_attribute("itemprop") == "Name":
                                return dt.text
                    elif sort_field == "Description":
                        dds = td.find_elements_by_tag_name("dd")
                        for dd in dds:
                            if dd.get_attribute("itemprop") == "Description":
                                return dd.text

    def check_sort_order(self, sort_field, asc_or_desc="desc"):
        error_found = False
        true_for_asc = asc_or_desc == "asc"
        print "Sort field: " + sort_field
        print "alpha fields: " + str(self.alpha_sort_fields)
        if sort_field not in self.valid_sort_fields:
            raise ValueError("Please sort by one of these: {l}".format(l=str(valid_sort_fields)))
        else:
            logging.info("Entering sort loop")
            prev_row = None
            prev_row_val = None
            curr_row = self.rows[0]
            curr_row_val = self.sort_value_for_row(curr_row, sort_field)
            index = 1
            while index < len(self.rows):
                prev_row =  curr_row
                prev_row_val = curr_row_val
                curr_row = self.rows[index]
                curr_row_val = self.sort_value_for_row(curr_row, sort_field)
                logging.debug("sorting by " + sort_field)
                logging.debug("prev_row_val: " + str(prev_row_val))
                logging.debug("curr_row_val: " + str(curr_row_val))
                #In date comparisons, later > earlier
                if asc_or_desc == "desc":
                    if prev_row_val < curr_row_val:
                        logging.error("Expected {b} >= {a} for desc {c}".format(a=str(curr_row_val), b=str(prev_row_val), c=sort_field))
                        return False
                else:
                    if prev_row_val > curr_row_val :
                        logging.error("Expected {b} <= {a} for asc {c}".format(a=str(curr_row_val), b=str(prev_row_val), c=sort_field))
                        return False
                index = index + 1
            return True

    def open_detail_view(self):
        details = self.driver.find_elements_by_class_name("resizer")
        for d in details:
            if d.text == "DETAIL":
                d.click()
                break

    def toggle_row_by_index(self, index):
        if not self.rows:
            self.refresh_table_rows()
        row = self.rows[index]
        start_class = row.get_attribute("class")
        tds = row.find_elements_by_tag_name("td")
        for td in tds:
            if td.get_attribute("itemprop") == "Owner":
                td.click()
                break
        max_wait_time = 5
        start_time = datetime.datetime.now()
        curr_time = datetime.datetime.now()
        is_ready = False
        while not is_ready and (curr_time - start_time) < datetime.timedelta(seconds=max_wait_time):
            if row.get_attribute("class") != start_class:
                is_ready = True
            time.sleep(0.2)

    def get_selected_row(self):
        if not self.is_something_selected():
            raise ValueError("There wasn't anything selected, cannot get selected row")
        index = 0
        while index < len(self.rows):
            if self.rows[index].get_attribute("class") == "active":
                return index
            index = index + 1
        raise ValueError("Got to end of rows, no selected one found.")

    def close_detail_view(self):
        closers = self.driver.find_elements_by_class_name("icon-down")
        for c in closers:
            if c.is_displayed():
                c.click()
                break

    def get_rows(self):
        return self.rows

    def is_something_selected(self):
        controls_divs = self.driver.find_elements_by_xpath("//div[@class='detailsControls']")
        print controls_divs[0].text
        if "Nothing selected." == controls_divs[0].text:
            return False
        else:
            return True

    def select_detail(self, field_name):
        if field_name.lower() not in self.valid_detail_tabs:
            raise ValueError("{d} not in {v}".format(d=field_name, v=self.valid_detail_tabs))
        aside = self.driver.find_element_by_css_selector("//aside[@class='workspace-detail attention']")
        aside.find_element_by_link_text(field_name)

class SimPage(GridPage):
    def __init__(self, driver):
        super(SimPage, self).__init__(driver, "COMPS: Explore: Simulations")
        self.valid_detail_tabs = self.valid_detail_tabs + ["files", "job", "output", "spatial"]

    def get_sorters(self):
        return self.sorters

    def get_relations_of_row(self, index, siblings_parent_children="sibling"):
        valid_relatives = ["siblings", "parent", "children"]
        if siblings_parent_children not in valid_relatives:
            raise ValueError("Please pick one of the following: " + str(valid_relatives) )
        row = self.rows[index]
        related_td = None
        for td in row.find_elements_by_tag_name("td"):
            if td.get_attribute("itemprop") == "Related":
                related_td = td
        if not related_td:
            raise ValueError("Row {i} had no related td.".format(i=index))
        links = related_td.find_elements_by_tag_name("a")
        for link in links:
            if link.get_attribute("rel") == siblings_parent_children:
                link.click()
                self.wait_for_ready()
                self.refresh_table_rows()
                return

class ExpPage(GridPage):
    def __init__(self, driver):
        super(ExpPage, self).__init__(driver, "COMPS: Explore: Experiments")

class StePage(GridPage):
    def __init__(self, driver):
        super(StePage, self).__init__(driver, "COMPS: Explore: Suites")

class DashboardPage(CompsPage):
    def __init__(self, driver):
        super(DashboardPage, self).__init__(driver, "COMPS: Dashboard")
        print self.load_time
        pass
        
    