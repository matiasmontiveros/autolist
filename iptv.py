import requests
import re
from github import Github

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
    
    for url in urls:
        try:
            response = requests.get(url)
            playbackurl = re.findall(r'playbackURL\s*":\s*"(https?://.*?\.m3u8\?token=.*?)"', response.text)
            if playbackurl:
                channel_name = url.split("=")[-1].replace("_", " ").capitalize()  # Extraer el nombre del canal
                playbackurls[channel_name] = playbackurl[0]
        except Exception as e:
            print(f"Error al procesar {url}: {e}")
    
    return playbackurls

def update_m3u_file(m3u_content, playbackurls):
    lines = m3u_content.splitlines()
    updated_content = []
    current_channel = None
    
    for line in lines:
        if line.startswith("#EXTINF:"):
            current_channel = line.split(",")[1].strip()  # Extraer el nombre del canal
            updated_content.append(line)
        elif current_channel in playbackurls:
            # Si el canal actual tiene una nueva URL, la reemplaza
            updated_content.append(playbackurls[current_channel])
            current_channel = None  # Reiniciar el nombre del canal
        else:
            updated_content.append(line)
    
    return "\n".join(updated_content)

def update_github_file(token, repo_name, file_path, content):
    g = Github(token)
    repo = g.get_user().get_repo(repo_name)

    try:
        file = repo.get_contents(file_path)
        repo.update_file(file_path, "Actualización de archivo .m3u", content, file.sha)
    except:
        repo.create_file(file_path, "Creación de archivo .m3u", content)

def process_and_update():
    # Suponiendo que tu archivo .m3u tiene los nombres correctos de los canales
    m3u_content = """
    #EXTM3U
    #EXTINF:-1, TNT Sports Argentina
    https://old-link-1.m3u8
    #EXTINF:-1, ESPN Premium
    https://old-link-2.m3u8
    #EXTINF:-1, TyC Sports
    https://old-link-3.m3u8
    """
    
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
