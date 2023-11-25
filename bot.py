import subprocess

def download_from_yt(url: str):
    process = subprocess.Popen(f"youtube-dl -f 'best[ext=mp4]' {url}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()

download_from_yt("https://www.youtube.com/watch?v=yHgx0DyzFcE")
