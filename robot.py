import pyautogui
import psutil
import pygetwindow as gw
import time
import os
from read_excel import trata_dados

def open_app(app):
    """Abre o Chrome e aguarda até que a janela esteja visível."""
    # Abrir o Chrome usando o atalho do Windows + R e digitando 'chrome'
    pyautogui.hotkey('win', 'r')
    time.sleep(1)  # Pequena pausa para garantir que a janela de execução abre
    pyautogui.write(app)
    pyautogui.press('enter')

    timeout = 10  # Tempo máximo de espera em segundos
    start_time = time.time()

    while time.time() - start_time < timeout:
        windows = gw.getWindowsWithTitle(app)
        if windows:
            for window in windows:
                if window.isMinimized:
                    window.restore()
                # Verifica se a janela está visível no primeiro plano
                if window.isActive:
                    print("Chrome está em execução e visível.")
                    return True
        time.sleep(0.5)

    print("Falha ao abrir o Chrome dentro do tempo limite.")
    return False

def verificar_processo(nome_processo):
    for processo in psutil.process_iter():
        if processo.name().lower() == F'{nome_processo}.exe':
            return True
        elif "EXCEL.EXE" == processo.name().upper():
            janelas_excel = gw.getWindowsWithTitle("Excel")
            if janelas_excel:
                return True
    return False

def fechar_processos():
    for tentativa in range(5):
        for processo in ['Chrome', 'Excel']:
            try:
                janela = gw.getWindowsWithTitle(processo)[0]
                print(f"{processo} está aberto, fechando para iniciar aplicação.")
                janela.close()
            except IndexError:
                pass
        return True

def get_info_terabyte(search_term):

    for search_term_in_site in search_term:

        if fechar_processos():

            open_app('chrome')


            # Maximiza tela
            pyautogui.hotkey('win', 'up')

            # Pesquisa site
            pyautogui.moveTo(1195, 63) 
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.write('https://www.terabyteshop.com.br/')
            pyautogui.press('enter')
            time.sleep(1)


            # Pesquisa o termo 
            pyautogui.moveTo(1195, 123) 
            time.sleep(0.5)
            pyautogui.click()
            pyautogui.write(search_term_in_site,)
            pyautogui.press('enter')
            time.sleep(3)

            for i in range(2):
                pyautogui.scroll(-100000)
                pyautogui.moveTo(900, 259) 
                pyautogui.click()
                time.sleep(2)

            # Define as coordenadas iniciais e finais
            x_inicial, y_inicial = 185, 400
            x_final, y_final = 130, 360

            pyautogui.scroll(1000000)
            time.sleep(1)

            # Simula o pressionamento do botão do mouse
            pyautogui.mouseDown(x=x_inicial, y=y_inicial)

            # Move o cursor do mouse para as coordenadas finais
            pyautogui.moveTo(x_final, y_final, duration=0.25)

            # Simula o botão do mouse sendo solto
            pyautogui.mouseUp(x=x_final, y=y_final)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'c')

        if open_app('excel'):

            # Alt + Espaço para abrir o menu de controle da janela
            pyautogui.hotkey('alt', 'space')
            pyautogui.press('x') # X para selecionar a opção de maximizar
            time.sleep(0.5)

            pyautogui.press('enter')
            time.sleep(0.5)

            pyautogui.hotkey('ctrl', 'v')
            time.sleep(5)

            pyautogui.hotkey('ctrl', 'b')
            time.sleep(0.5)
            # Obter a estrutura de tempo atual
            estrutura_tempo = time.localtime()

            # Formatar a data e hora

            date_time = time.strftime("%Y%m%d", estrutura_tempo)
            pyautogui.write(f'extraction_processadores_{date_time}') if 'Processador' in search_term_in_site else pyautogui.write(f'extraction_placavideo_{date_time}')
            time.sleep(0.5)
            pyautogui.press('enter')
            fechar_processos()

get_info_terabyte(search_term = ['Processador', 'Placa de video'])
time.sleep(2)
list_files = [c for c in os.listdir('raw_data/')]

trata_dados(list_files)







