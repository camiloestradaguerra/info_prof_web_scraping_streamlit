import os, json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

def _get_data_profesionales(documento_cedula: str):
    """
    Obtiene los datos de los profesionales con sus respectivas sanciones
    :param documento_cedula: documento del que se desea obtener la informacion
    :return: dataframe con los datos del profesional
    """
    path = os.getcwd()
    driver_path = '{}\chromedriver'.format(path)
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s)
    driver.get("https://administrador.consejoapp.com.co/index.php/consultas/profesionales")
    driver.maximize_window()

    ced = driver.find_element(By.XPATH, '//*[@id="cedula"]')
    ced.send_keys(documento_cedula)
    ced.send_keys(Keys.ENTER)

    ver_boton = driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/td[5]/a')
    ver_boton.click()

    json_file1 = {
                    'Nombres' : driver.find_element(By.XPATH, '/html/body/div/div/div[2]/table/tbody/tr[1]/td').text,
                    'Apellidos' : driver.find_element(By.XPATH, '/html/body/div/div/div[2]/table/tbody/tr[2]/td').text,
                    'Titulo' : driver.find_element(By.XPATH, '/html/body/div/div/div[2]/table/tbody/tr[3]/td').text,
                    'Universidad' : driver.find_element(By.XPATH, '/html/body/div/div/div[2]/table/tbody/tr[4]/td').text,
                    'Matricula' : driver.find_element(By.XPATH, '/html/body/div/div/div[2]/table/tbody/tr[5]/td').text,
                    'Acta' : driver.find_element(By.XPATH, '/html/body/div/div/div[2]/table/tbody/tr[6]/td').text
                    }
        
    driver.get("https://administrador.consejoapp.com.co/index.php/consultas/sanciones")

    ced = driver.find_element(By.XPATH, '//*[@id="cedula"]')
    ced.send_keys(documento_cedula)
    ced.send_keys(Keys.ENTER)

    ver_boton = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[3]/div/button')
    ver_boton.click()

    json_file2 = {
                    'Tipo de Sanción' : driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/td[3]').text,
                    'Motivo' : driver.find_element(By.XPATH,'/html/body/div[2]/table/tbody/tr/td[4]').text,
                    'Fecha de Inicio' : driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/td[5]').text,
                    'Tiempo (Días)' : driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/td[6]').text,
                    'Fecha de resolución' : driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/td[7]').text
                    }

    json_file = json_file1.copy()
    json_file.update(json_file2)

    df = pd.DataFrame([json_file])
    return df.T