from datetime import datetime
from urllib import request
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

class Bot:
    def __init__(self) -> None:
        user_agent = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'''
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--allow-insecure-localhost')
        self.options.add_argument('acceptInsecureCerts')
        self.options.add_argument('--ignore-certificate-errors')
        
        self.options.add_experimental_option('prefs', {
        "download.default_directory": r'./', #Pasta onde serão salvos os arquivos
        "download.prompt_for_download": False, #parâmetro para baixar o arquivo automaticamente
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        
        self.driver = webdriver.Chrome(service=Service (ChromeDriverManager().install()), options=self.options)
        
        self.driver.get("https://imprensaoficial.al.gov.br/diario-oficial")
        
        hoje = datetime.today().strftime("%d.%m.%Y")
        # Setup wait for later
        # wait = WebDriverWait(self.driver, 10)

        # Store the ID of the original window
        original_window = self.driver.current_window_handle

        # Checar se não existem outras janelas abertas
        assert len(self.driver.window_handles) == 1

        self.driver.get_screenshot_as_file('screenshot.png') # salva um print do site

        link_diario = self.driver.find_element(By.XPATH, '//*[@id="tagBody"]/main/section/div[1]/div/section/div[3]/div[1]/article/div/div[3]/a[2]') # pega o elemento do dom que contém o link pro pdf
       # link_diario = self.driver.find_element(By.XPATH, '//*[@id="miniaturas"]/table/tbody/tr/td[1]/a')
        print(link_diario.get_attribute('href'))
        
        sleep(5)
        
        # self.driver.get(link_diario.get_attribute('href'))   

        self.save_pdf(link_diario.get_attribute('href'), hoje)

    def save_pdf(self, link, filename):
    
        response = request.urlopen(link)    
        print("salvando")
        # print(response.read())
        file = open("./"+filename , 'wb')
        print(file)
        print(f"salvando em do_alagoas_{filename}.pdf")
        file.write(response.read())
        file.close()

        sleep(25) # substituir por espera automática do final do download


Bot()
