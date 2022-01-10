from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_binary
import csv
import time
import pyperclip


def read_csv(filename):
    results = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            results.append(row)
    return results


class BotWhatsapp:
    def __init__(self, web_whatsapp_url, path_contacts, path_messages):
        self.web_whatsapp_url = web_whatsapp_url
        self.timeout = 30
        self.targets = read_csv(path_contacts)
        self.messages = read_csv(path_messages)
        self.__set_paths()

    def __set_paths(self):
        self.search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        self.input_xpath = '//div[@contenteditable="true"][@data-tab="9"]'
        self.contact_xpath = (
            '//span[@title="{0}"]'  # Hay que pasarle con .format() el contacto
        )
        self.first_contact = '//*[@id="pane-side"]/div[1]/div/div/div[1]'

    def __start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-plugins-discovery")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Se utiliza si hay que utilizar el driver de algun lugar especifico
        # pero en este caso estamos utilizando el paquete chromedriver_binary para cargar el driver

        # self.browser = webdriver.Chrome(executable_path=self.path_driver,
        #                                 chrome_options=options)
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.browser.get(self.web_whatsapp_url)
        try:
            # wait = WebDriverWait(driver, 10)
            self.wait5 = WebDriverWait(self.browser, 5)
            input("Escanea el código QR y presiona Enter")
            self.wait5.until(
                EC.presence_of_element_located((By.XPATH, self.search_xpath))
            )
            return True
        except Exception as e:
            print(e)
            return False

    def send_messages(self):
        start = self.__start_browser()
        if not start:
            return False
        
        for contact in self.targets:
            user_search = self.__search_user_or_group(contact["contact_name"])
            if not (user_search or contact):
                return False
            
            for msg_to in self.messages:
                message = msg_to["message"].strip()
                try:
                    input_box = self.wait5.until(
                        EC.presence_of_element_located(
                            (By.XPATH, self.input_xpath)
                        )
                    )
                except Exception as e:
                    print(e)
                    return
                messages = message.split("\\n")
                
                for i in range(int(msg_to["quantity"])):
                    for msg in messages:
                        pyperclip.copy(msg)
                        input_box.send_keys(Keys.SHIFT, Keys.INSERT)
                        input_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    
                    time.sleep(2)
                    input_box.send_keys(Keys.ENTER)
                print(f'Mensajes enviado a {contact["contact_name"]}.')

        return True
    
    def __search_user_or_group(self, contact):
        # Select the target
        search_box = self.wait5.until(
            EC.presence_of_element_located((By.XPATH, self.search_xpath))
        )
        search_box.clear()
        time.sleep(1)
        pyperclip.copy(contact)

        search_box.send_keys(Keys.SHIFT, Keys.INSERT)
        print(f"El contacto {contact} se seleccionó correctamente")

        try:
            vali_ = self.wait5.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.first_contact)
                )
            )
            if vali_.is_displayed():
                search_box.send_keys(Keys.ENTER)
                return True
        except Exception as e:
            print(e)
            print(f'No se encontró el contacto {contact}.')
        return False


obj = BotWhatsapp(
    "https://web.whatsapp.com/", "resources/contacts.csv", "resources/messages.csv"
)
obj.send_messages()
# obj.quit_browser()
