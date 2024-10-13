import requests
import re
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
    
    playbackurls = []
    
    for url in urls:
        try:
            response = requests.get(url)
            # Nueva expresión regular para extraer el playbackURL
            playbackurl = re.findall(r'var playbackURL\s*=\s*"(https?://.*?\.m3u8\?token=.*?)"', response.text)
            if playbackurl:
                playbackurls.append(playbackurl[0])
            else:
                print(f"No se encontró playbackURL en {url}")
        except Exception as e:
            print(f"Error al procesar {url}: {e}")
    
    return playbackurls

def update_m3u_file(m3u_content, playbackurls):
    for i, url in enumerate(playbackurls, start=1):
        m3u_content = m3u_content.replace(f"#EXTINF:-1,Canal {i}\n\n", f"#EXTINF:-1,Canal {i}\n{url}\n")
    return m3u_content

def update_github_file(token, repo_name, file_path, content):
    g = Github(token)
    repo = g.get_user().get_repo(repo_name)

    try:
        file = repo.get_contents(file_path)
        repo.update_file(file_path, "Actualización de archivo .m3u", content, file.sha)
        print(f"Archivo {file_path} actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar el archivo {file_path}: {e}")
        try:
            repo.create_file(file_path, "Creación de archivo .m3u", content)
            print(f"Archivo {file_path} creado correctamente.")
        except Exception as e:
            print(f"Error al crear el archivo {file_path}: {e}")

def process_and_update():
    m3u_content = "#EXTM3U\n#EXTINF:-1,Canal 1\n\n#EXTINF:-1,Canal 2\n\n"
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
