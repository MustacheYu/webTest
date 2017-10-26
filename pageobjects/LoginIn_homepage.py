# encoding=utf-8
from base_page import BasePage


class HomePage(BasePage):

    def send_username(self, text):
        self.type("LoginPage", "login_username_input", text)

    def send_password(self, text):
        self.type("LoginPage", "login_password_input", text)

    def send_checkcode(self, text):
        self.type("LoginPage", "login_checkcode_input", text)

    def send_submit_btn(self):
        self.click("LoginPage", "search_submit_btn")
