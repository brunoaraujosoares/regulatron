from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# funções do webdriver
def get_driver() -> webdriver:
    """
    Retorna um objeto WebDriver para o Chrome.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()),
                              options = options)    
    
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
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.ID, element_id)))
