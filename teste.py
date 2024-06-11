from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import time

# Caminho para o perfil do seu navegador pessoal
profile_path = 'C:/Users/Eduardo Oliveira/AppData/Local/Google/Chrome/User Data'

# Configura o ChromeOptions com o perfil do seu navegador pessoal
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--incognito')
chrome_options.add_argument('--user-data-dir=' + profile_path)

# Inicializa o webdriver para o Chrome com as ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Navega até uma URL com o popup
driver.get('https://www.terabyteshop.com.br/')

# Espera até que o popup seja exibido
try:
    modal_content = WebDriverWait(driver, 7).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'modal-content'))
    )
    pyautogui.moveTo(400, 259) 
    pyautogui.click()

except TimeoutException:
    print('Pop-up não abriu')

# Localiza a barra de pesquisa pelo ID (substitua 'id_da_barra_de_pesquisa' pelo ID real)
barra_de_pesquisa = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'isearch'))
)
# Insere um termo de pesquisa na barra de pesquisa
barra_de_pesquisa.send_keys('Placa de vídeo')
barra_de_pesquisa.send_keys(Keys.RETURN)

# Aguarda o carregamento da página após a pesquisa
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'container'))
)
for i in range(1):
    time.sleep(2)
    driver.execute_script("document.getElementById('pdmore').click();")

time.sleep(2)
    

x_inicial, y_inicial = 178, 459
x_final, y_final = 107, 430

# Simula o pressionamento do botão do mouse
pyautogui.mouseDown(x=x_inicial, y=y_inicial)
# Move o cursor do mouse para as coordenadas finais
pyautogui.moveTo(x_final, y_final, duration=0.2)
# Simula o botão do mouse sendo solto
pyautogui.mouseUp(x=x_final, y=y_final)
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'c')
