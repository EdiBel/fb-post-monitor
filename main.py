import os
import requests
from bs4 import BeautifulSoup

C_USER = os.getenv("C_USER")
XS = os.getenv("XS")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LAST_ID_FILE = "last_post_id.txt"

def get_last_post_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    return None

def set_last_post_id(post_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(post_id)

def check_group():
    cookies = {'c_user': C_USER, 'xs': XS}
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://www.facebook.com/groups/fuadex/?sorting_setting=CHRONOLOGICAL"
    res = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        if '/groups/fuadex/permalink/' in a['href']:
            pid = a['href'].split('/')[-2]
            link = 'https://www.facebook.com' + a['href']
            if pid != get_last_post_id():
                set_last_post_id(pid)
                send_message(f"📢 פוסט חדש בקבוצת פואד:\n{link}")
            break

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    check_group()
