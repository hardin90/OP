from common import BasePage
from selenium.webdriver.common.by import By


username = 'admin'
password = 'g15FPPKf'
host = '10.11.3.80'


class ObjectsLocs():
    node = "//div[@id='ext-comp-1238']"
#1.Buttons
    B_first_page = node + "//button[contains(@class,'x-tbar-page-first')]"
    B_prev_page = node + "//button[contains(@class,'x-tbar-page-prev')]"
    B_next_page = node + "//button[contains(@class,'x-tbar-page-next')]"
    B_last_page = node + "//button[contains(@class,'x-tbar-page-next')]"
    B_refresh_page = node + "//button[contains(@class,'x-tbar-loading')]"
    B_search_page = node + "//img[contains(@class,'x-form-search-trigger')]"
    B_filter = node + "//img[contains(@class,'x-form-arrow-trigger')]"
    B_user = node + "//button[contains(@class,'icon-user-suit')]"
    B_users_project = node + "//button[contains(@class,'icon-folder')]"
    B_user_logs = node + "//button[contains(@class,'icon-monitor')]"
    B_console = node + "//button[contains(@class,'icon-term')]"
    B_migration_state = node + "//button[contains(@class,'icon-migration')]"
# 2.Buttons Servers
    B_servers = node + "//button[contains(@class,'icon-computer')]"
    B_vm_create = ""
    B_vm_power_off = ""
    B_vm_power_on = ""
    B_vm_reboot = ""
    B_vm_console = ""
    B_vm_rename = ""
    B_vm_delete = ""
    B_vm_copy = ""
    B_vm_network = ""
    B_vm_migration = ""
    B_vm_change_flavors = ""
    B_vm_accept_change_flavors = ""
    B_vm_change_state = ""
    B_vm_evacuation = ""
#3.Buttons Disks
    B_disks = node + "//button[contains(@class,'icon-drive')]"
    B_disks_create = ""
    B_disks_edit = ""
    B_disks_mount = ""
    B_disks_copy = ""
    B_disks_unmout = ""
    B_disks_delete = ""
#4.Select
    S_filter = "//div[contains(@class,'x-combo-list-item') and text()='%s']"
#5. Input Fields
    F_filter_field = "//input[@name='subj']"


class Select(BasePage):
    def vm(self):
        pass

    def disk(self):
        pass

    def vm_copy(self):
        pass

    def disk_copy(self):
        pass

class Get(BasePage):
    def header_title(self):
        pass

    def id(self):
        pass

    def name(self):
        pass

    def flavors(self):
        pass

    def vcpu(self):
        pass

    def ram(self):
        pass

    def hdd(self):
        pass

    def host(self):
        pass

    def status(self):
        pass

    def date(self):
        pass

    def type(self):
        pass

    def migration(self):
        pass

    def login_name(self):
        pass

    def project(self):
        pass


class Buttons(BasePage):
    # def __init__(self):
    #     self.server = Servers_buttons
    #     self.disks = Disks_buttons

    def first_page(self):
        return self.click(self.find_element(ObjectsLocs.B_first_page))


    def prev_page(self):
        return self.click(self.find_element(ObjectsLocs.B_prev_page))

    def next_page(self):
        return self.click(self.find_element(ObjectsLocs.B_next_page))

    def last_page(self):
        return self.click(self.find_element(ObjectsLocs.B_last_page))

    def refresh(self):
        return self.click(self.find_element(ObjectsLocs.B_refresh_page))

    def search(self):
        return self.click(self.find_element(ObjectsLocs.B_search_page))

    def filter(self, value):
        filer_id = self.get_att(ObjectsLocs.F_filter_field, 'id')
        if self.execute_script("Ext.getCmp('%s').lastSelectionText" % filer_id) is value:
            print(self.execute_script("Ext.getCmp('%s').lastSelectionText" % filer_id))
            self.refresh()
        else:
            self.click(self.find_element(ObjectsLocs.B_filter))
            self.click(self.find_element(ObjectsLocs.S_filter % value))
            self.refresh()

    def users(self):
        pass

    def projects_users(self):
        pass

    def logs_users(self):
        pass

    def console(self):
        pass

    def migration(self):
        pass

class Servers_buttons(BasePage):
    def create(self):
        pass

    def power_off(self):
        pass

    def reboot(self):
        pass

    def console(self):
        pass

    def rename(self):
        pass

    def delete(self):
        pass

    def copy(self):
        pass

    def network(self):
        pass

    def migration(self):
        pass

    def change_flavors(self):
        pass

    def accept_flavors(self):
        pass

    def change_state(self):
        pass

    def evacation(self):
        pass

class Disks_buttons(BasePage):
    def create(self):
        pass

    def edit(self):
        pass

    def mount(self):
        pass

    def copy(self):
        pass

    def unmount(self):
        pass

    def delete(self):
        pass

class VM(BasePage):
    def create(self):
        pass


    # def enter_word(self, word):
    #     search_field = self.find_element(YandexSeacrhLocators.LOCATOR_YANDEX_SEARCH_FIELD)
    #     search_field.click()
    #     search_field.send_keys(word)
    #     return search_field
    #
    # def click_on_the_search_button(self):
    #     return self.find_element(YandexSeacrhLocators.LOCATOR_YANDEX_SEARCH_BUTTON,time=2).click()
    #
    # def check_navigation_bar(self):
    #     all_list = self.find_elements(YandexSeacrhLocators.LOCATOR_YANDEX_NAVIGATION_BAR,time=2)
    #     nav_bar_menu = [x.text for x in all_list if len(x.text) > 0]
    #     return nav_bar_menu

class Disks(BasePage):
    def create(self):
        pass