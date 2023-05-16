from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.proxy import Proxy, ProxyTyhpe
# https://hidemy.name/en/proxy-list/

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# funções do webdriver
def get_driver() -> webdriver:
    """
    Retorna um objeto WebDriver para o Chrome.
    """
    software_names    = [SoftwareName.CHROME.value]
    options = webdriver.ChromeOptions()

    operating_systems = [
                            OperatingSystem.WINDOWS.value,
                            OperatingSystem.LINUX.value
            	        ]
    user_agent_rotator = UserAgent(
                            software_names = software_names,
                            operating_systems = operating_systems, 
                            limit = 100
                            )
    user_agent = user_agent_rotator.get_random_user_agent()

    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox') 
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()),
                              options = options) 
    driver.implicitly_wait(5)
    driver.maximize_window()# Maximiza a janela
    
    return driver

def navigate_to_page(driver: webdriver, url: str) -> None:
    """
    Navega para uma determinada URL no navegador.
    """
    driver.get(url)
    

def search(driver: webdriver, query: str, element_id: str) -> None:
    """
    Busca por query no element_id informado.
    """
    search_box = driver.find_element(By.ID, element_id)
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)


def element_exists(driver: webdriver, element_id: str) -> bool:
    """
    Verifica se um elemento com o ID especificado existe na página.
    """
    try:
        driver.find_element(By.ID, element_id)
        return True
    except:
        return False


def wait_for_element(driver: webdriver, element_id: str, timeout: int = 2) -> None:
    """
    Aguarda até que um elemento com o ID especificado seja carregado na página.
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.ID, element_id)))
    except:
        pass
