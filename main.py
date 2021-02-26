# logics

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
import json, random
from datetime import datetime

Builder.load_file('design.kv')

class LoginScreen(Screen, App):
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"

    def fade_text(self):
        self.ids.login_wrong.text = ""

    def login(self, username, password):
        try:
            with open("users.json") as file:
                users = json.load(file)
        except FileNotFoundError:
            self.ids.login_wrong.text = "No one has registered yet! >_<"
            Clock.schedule_once(lambda dt: self.fade_text(), 1)
        else:
            if username in users and users[username]['password'] == password:
                self.manager.transition.direction = "left"
                self.manager.current = "login_screen_success"
            else:
                self.ids.login_wrong.text = "Wrong username or password!"
                Clock.schedule_once(lambda dt: self.fade_text(), 1)

    def forget_password(self):
        try:
            with open("users.json") as file:
                pass
        except FileNotFoundError:
            self.ids.login_wrong.text = "No one has registered yet! >_<"
            Clock.schedule_once(lambda dt: self.fade_text(), 1)
        else:
            self.manager.transition.direction = "left"
            self.manager.current = "set_new_password"

class SignUpScreen(Screen):
    def add_user(self, username, password):
        try:
            with open("users.json") as file:
                users = json.load(file)
        except FileNotFoundError:
            with open("users.json", "w") as file:
                users = {}

        users[username] = {
            "username": username, "password": password,
                        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        }

        with open("users.json", "w") as file:
            json.dump(users, file)
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen_success"

    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        try:
            with open(f"quotes/{feel.split()[0]}.txt", encoding="utf-8") as file:
                quotes = file.readlines()

        except FileNotFoundError:
            self.ids.quote.text = "Try something else..."
        else:
            self.ids.quote.text = random.choice(quotes)
            self.ids.scrollview.scroll_y = 1


# ButtonBehavior must be first
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class NewPassword(Screen):
    def fade_text(self):
        self.ids.inform.text = ""

    def reset(self, username, password):
        self.ids.inform.text = ""
        with open("users.json") as file:
            users = json.load(file)

        try:
            users[f"{username}"]['password'] = password
        except KeyError:
            self.ids.inform.text = 'This user does not exist!'
            Clock.schedule_once(lambda dt: self.fade_text(), 1)
        else:
            with open("users.json", 'w') as file:
                json.dump(users, file)
            self.manager.transition.direction = "right"
            self.manager.current = "login_screen"

    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
