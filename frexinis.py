import requests
import time
from colorama import Fore, init

init(autoreset=True)

text = """
██████╗  ██████╗ ██████╗ ██╗      ██████╗ ██╗  ██╗
██╔══██╗██╔═══██╗██╔══██╗██║     ██╔═══██╗╚██╗██╔╝
██████╔╝██║   ██║██████╔╝██║     ██║   ██║ ╚███╔╝ 
██╔══██╗██║   ██║██╔══██╗██║     ██║   ██║ ██╔██╗ 
██║  ██║╚██████╔╝██████╔╝███████╗╚██████╔╝██╔╝ ██╗
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
"""

print(Fore.YELLOW + text)

try:
    user_id = int(input("Takipçi Göndereceğiniz Hesabın ID'sini Girin: "))
    follow_count = int(input("Kaç Adet Takipçi Göndericeksiniz: "))
except ValueError:
    print(Fore.RED + "[ERROR]: Lütfen Sayı Halinde Girin!")
    exit()

def proxies():
    proxy_url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all&ssl=all&anonymity=all"
    try:
        proxy_response = requests.get(proxy_url)
        proxies_list = proxy_response.text.splitlines()
        return proxies_list if proxies_list else []
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[ERROR]: Proxy API İle İletişime Geçilemedi - {str(e)}")
        return []

try:
    with open('cookies.txt', 'r') as cookie_file:
        cookies = cookie_file.read().splitlines()
except FileNotFoundError:
    print(Fore.RED + "[ERROR]: 'cookies.txt' Dosyası Projede Yok!")
    exit()

if not cookies:
    print(Fore.RED + "[ERROR]: 'cookies.txt' Dosyası Boş!")
    exit()

def csrf_token(cookie):
    headers = {
        'Cookie': f'.ROBLOSECURITY={cookie}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    try:
        response = requests.get('https://www.roblox.com/home', headers=headers)
        csrf_token = response.cookies.get('.ROBLOX.CSRF')
        return csrf_token if csrf_token else None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[ERROR]: Bağlantı Hatası- {str(e)}")
        return None

def follow(user_id, cookie, csrf_token, proxy):
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    headers = {
        'Cookie': f'.ROBLOSECURITY={cookie}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Content-Type': 'application/json',
        'x-csrf-token': csrf_token
    }

    try:
        r = requests.post(f'https://friends.roblox.com/v1/users/{user_id}/follow', headers=headers, proxies=proxy_dict)
        if r.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

proxies_list = proxies()
if not proxies_list:
    print(Fore.RED + "[ERROR]: Proxy Listesi Alınamadı!")
    exit()

successs = 0
failed = 0

for cookie in cookies:
    try:
        csrf_token = csrf_token(cookie)
        if not csrf_token:
            continue

        for proxy in proxies_list:
            if  successs >= follow_count:
                break

            success = follow(user_id, cookie, csrf_token, proxy)
            if success:
                successs += 1
                print(Fore.GREEN + f"[SUCCESS]: {successs} Takipçi Gönderildi1")
            else:
                failed += 1
                print(Fore.RED + f"[ERROR]: Proxy '{proxy}' İle Takipçi Gönderilemedi!")

            time.sleep(30)

    except Exception as e:
        failed += 1
        print(Fore.RED + f"[ERROR]: Beklenmeyen Hata - {str(e)}")
        continue

print(Fore.GREEN + f"[INFO] Başarıyla Gönderilen Takipçi Sayısı: {successs}")
print(Fore.RED + f"[INFO] Başarısız Olan Takipçi Sayısı: {failed}")
