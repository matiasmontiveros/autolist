import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from github import Github
import os

def extract_playbackurl():
    urls = [
        "https://streamtp1.com/global1.php?stream=tntsports_argentina",
        "https://streamtp1.com/global1.php?stream=espn_premium",
        "https://streamtp1.com/global1.php?stream=tyc_sports",
        "https://streamtp1.com/global1.php?stream=dsports",
        "https://streamtp1.com/global1.php?stream=dsports_2",
        "https://streamtp1.com/global1.php?stream=dsports_plus",
        "https://streamtp1.com/global1.php?stream=fox1ar",
        "https://streamtp1.com/global1.php?stream=fox2ar",
        "https://streamtp1.com/global1.php?stream=fox3ar",
        "https://streamtp1.com/global1.php?stream=espn1",
        "https://streamtp1.com/global1.php?stream=espn2",
        "https://streamtp1.com/global1.php?stream=espn3",
        "https://streamtp1.com/global1.php?stream=espn4",
        "https://streamtp1.com/global1.php?stream=espn5",
        "https://streamtp1.com/global1.php?stream=espn6",
        "https://streamtp1.com/global1.php?stream=espn7",
        "https://streamtp1.com/global1.php?stream=winplus",
        "https://streamtp1.com/global1.php?stream=tnt_chile"
    ]
    
    playbackurls = {}

    # Configurar Selenium en modo headless para no abrir el navegador visualmente
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Headers a incluir en las solicitudes
    headers = {
        "Referer": "https://streamtp1.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

    try:
        # Intentar instalar y obtener el path de chromedriver
        chromedriver_path = ChromeDriverManager().install()
        print(f"chromedriver está disponible en: {chromedriver_path}")
        
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

        for url in urls:
            try:
                # Usar Selenium para cargar la página
                driver.get(url)
                print(f"Accediendo a {url} con Selenium")

                # Esperar hasta que el elemento que contiene el playbackURL esté presente
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="elemento_que_contiene_playbackURL"]')))

                # Usar Selenium para buscar el playbackURL
                page_source = driver.page_source
                playbackurl = re.findall(r'var\s+playbackURL\s*=\s*"(https?://.*?\.m3u8\?token=.*?)"', page_source)

                if playbackurl:
                    channel_name = url.split("=")[-1].replace("_", " ").capitalize()
                    playbackurls[channel_name] = playbackurl[0]
                    print(f"Encontrado playbackURL con Selenium para {channel_name}")
                else:
                    print(f"No se encontró playback URL para: {url} con Selenium")
            except Exception as e:
                print(f"Error al procesar {url} con Selenium: {e}")
    except Exception as e:
        print(f"Error al instalar o obtener chromedriver: {e}")
    
    driver.quit()
    
    return playbackurls

def update_m3u_file(m3u_content, playbackurls):
    for channel_name, url in playbackurls.items():
        m3u_content = m3u_content.replace(f"#EXTINF:-1,{channel_name}\n\n", f"#EXTINF:-1,{channel_name}\n{url}\n")
    return m3u_content

def update_github_file(token, repo_name, file_path, content):
    g = Github(token)
    repo = g.get_user().get_repo(repo_name)

    try:
        file = repo.get_contents(file_path)
        repo.update_file(file_path, "Actualización de archivo .m3u", content, file.sha)
    except:
        repo.create_file(file_path, "Creación de archivo .m3u", content)

def process_and_update():
    m3u_content = "#EXTM3U\n" + "\n".join([f"#EXTINF:-1,{url.split('=')[-1].replace('_', ' ').capitalize()}\n\n" for url in [
        "https://streamtp1.com/global1.php?stream=tntsports_argentina",
        "https://streamtp1.com/global1.php?stream=espn_premium",
        "https://streamtp1.com/global1.php?stream=tyc_sports",
        "https://streamtp1.com/global1.php?stream=dsports",
        "https://streamtp1.com/global1.php?stream=dsports_2",
        "https://streamtp1.com/global1.php?stream=dsports_plus",
        "https://streamtp1.com/global1.php?stream=fox1ar",
        "https://streamtp1.com/global1.php?stream=fox2ar",
        "https://streamtp1.com/global1.php?stream=fox3ar",
        "https://streamtp1.com/global1.php?stream=espn1",
        "https://streamtp1.com/global1.php?stream=espn2",
        "https://streamtp1.com/global1.php?stream=espn3",
        "https://streamtp1.com/global1.php?stream=espn4",
        "https://streamtp1.com/global1.php?stream=espn5",
        "https://streamtp1.com/global1.php?stream=espn6",
        "https://streamtp1.com/global1.php?stream=espn7",
        "https://streamtp1.com/global1.php?stream=winplus",
        "https://streamtp1.com/global1.php?stream=tnt_chile"
    ]])
    
    playbackurls = extract_playbackurl()
    if playbackurls:
        m3u_content = update_m3u_file(m3u_content, playbackurls)
        token = os.getenv("TOKEN")  # Acceder al token desde un entorno seguro
        repo_name = "lista.m3u"
        file_path = "lista.m3u"
        update_github_file(token, repo_name, file_path, m3u_content)
    else:
        print("No se encontraron playback URLs para actualizar.")

# Ejecutar el script una vez
process_and_update()
