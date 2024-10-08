import requests
import re
import schedule
import time
from github import Github
def extract_playbackurl():
    urls = [
    "https://streamtp1.com/global1.php?stream=tntsports_argentina",
    "https://streamtp1.com/global1.php?stream=espn_premium",
    "https://streamtp1.com/global1.php?stream=tyc_sports"
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
    "https://streamtp1.com/global1.php?stream=tnt_chile",
    ]
    playbacksurls = []
    for url in urls:
        try:
            response =
            requests.get(url)
            playbackurl =
            re.findall(r'playbackURL\s*":\s*"(https?://.*?\.m3u8\?token=.*?)"',
                       response.text)
            if playbackurl:
                
    playbackurls.append(playbackurl[0])
                except Exception as e:
                    print(f"error al procesar {url}: {e}")
                    return playbackurls
                playbackurls = extract_playbackurl()

    for i, url in
    enumerate(playbackurls, start=1):
        print(f"playback URL Canal {i}:{url}")
        m3u_content =
        m3ucontent.replace(f"#EXTINF:-1,Canal {i}\n\n", f"#EXTINF:-1,Canal {i}\n{url}\n")
        print("contenido final del archivo .m3u:")
        print(m3u_content)

    def update_github_file(token, repo_name, file_path, content):
        g = github(token)
        repo =
        g.get_user().get_repo(repo_name)

        try:
            file =
            repo.get_contents(file_path)
            repo.upddate_file(file_path, "actualización de archivo .m3u", content, file.sha)
        except:
            repo.create_file(file_path, "creación de archivo .m3u", content)

    def update_m3u_file(m3u_content, channel_name, playbackurl, position):
        lines = m3u_content.splitlines()
        lines[position] = f'#EXTINF:-1,{channel_name}\n{playbackurl}'
        return"\n".join(lines)
    def process_and_updates():
        channel_positions = {
            "Canal 1": 2,
            "Canal 2": 4,
            "Canal 3": 6,
            "Canal 4": 8,
            "Canal 5": 10,
            "Canal 6": 12,
            "Canal 7": 14,
            "Canal 8": 16,
            "Canal 9": 18,
            "Canal 10": 20,
            "Canal 11": 22,
            "Canal 12": 24,
            "Canal 13": 26,
            "Canal 14": 28,
            "Canal 15": 30,
            "Canal 16": 32,
            "Canal 17": 34,
            "Canal 18": 36,
            }
    m3u_content =
    "#EXTM3U\n#EXTINF:-1,Canal 1\n\n#EXTINF:-1,Canal 2\n\n"
    token = "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"
    repo_name = "lista.m3u"
    file_path = "lista.m3u"

    update_github_file(token, repo_name, file_path, m3u_content)

    schedule.every(3).hours.do(process_and_update)
    while true:
        schedule.run_pending()
        time.sleep(1)
