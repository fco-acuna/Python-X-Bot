import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


class TwitterBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.bot = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.is_logged_in = False

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(4)

        try:
            email_input = bot.find_element(By.NAME, "text")
            email_input.clear()
            email_input.send_keys(self.email)
            email_input.send_keys(Keys.RETURN)
            time.sleep(2)

            # A veces pide el username después del email, a veces no
            try:
                username_input = bot.find_element(By.NAME, "text")
                username_input.clear()
                username_input.send_keys("@dog_daily71350")
                username_input.send_keys(Keys.RETURN)
                time.sleep(2)
            except NoSuchElementException:
                pass

            password_input = bot.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)

            self.is_logged_in = True
        except NoSuchElementException as e:
            print("Error en el login:", e)
            self.is_logged_in = False

    def logout(self):
        if not self.is_logged_in:
            return

        bot = self.bot
        bot.get('https://twitter.com/home')
        time.sleep(4)

        try:
            bot.find_element(By.XPATH, "//div[@data-testid='SideNav_AccountSwitcher_Button']").click()
            time.sleep(1)
            bot.find_element(By.XPATH, "//a[@data-testid='AccountSwitcher_Logout_Button']").click()
            time.sleep(3)
            bot.find_element(By.XPATH, "//div[@data-testid='confirmationSheetConfirm']").click()
        except NoSuchElementException:
            print("No se pudo cerrar sesión correctamente.")

        time.sleep(3)
        self.is_logged_in = False

    @staticmethod
    def download_image(url, filename="temp.jpg"):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return os.path.abspath(filename)

    def post_tweets(self, tweet_body, image_url=None):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        try:
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()
        except NoSuchElementException:
            time.sleep(3)
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(4)

        try:
            tweet_box = bot.find_element(By.XPATH, "//div[@role='textbox']")
        except NoSuchElementException:
            time.sleep(3)
            tweet_box = bot.find_element(By.XPATH, "//div[@role='textbox']")

        tweet_box.send_keys(tweet_body)
        time.sleep(1)

        # ↓↓↓ Agregar imagen si se proporciona URL ↓↓↓
        if image_url:
            image_path = self.download_image(image_url)
            file_input = bot.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(image_path)
            time.sleep(2)

        # Enviar tweet
        tweet_button_css_selector = bot.find_element(By.XPATH, "//button[contains(@class, 'r-1cwvpvk')]")

        

        try:
            tweet_button = WebDriverWait(bot, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.r-1cwvpvk"))
            )
            time.sleep(5)
            tweet_box.send_keys(Keys.ESCAPE)
            tweet_button.click()
            print("✅ Tweet enviado exitosamente!")
        except Exception as e:
            print(f"❌ Ocurrió un error al publicar el tweet: {e}")

        time.sleep(4)

        # Limpieza: eliminar imagen temporal
        if image_url and os.path.exists(image_path):
            os.remove(image_path)
