import asyncio
import random
import ssl
import json
import time
import uuid
import requests
import argparse
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from colorama import init, Fore, Style
import itertools
import sys

# Initialize colorama
init(autoreset=True)

# ANSI escape codes for colors
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
BRIGHT = Style.BRIGHT
RESET = Style.RESET_ALL

# Function to fetch proxies from the URL
def fetch_proxies(url):
    proxies = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            proxies = response.text.strip().split('\n')
    except Exception as e:
        logger.error(f"Failed to fetch proxies: {e}")
    return proxies

# Function to show animated loading
def animated_loading(message):
    chars = "/—\|"
    for char in itertools.cycle(chars):
        sys.stdout.write('\r' + message + char)
        sys.stdout.flush()
        time.sleep(0.1)

# Function to display welcome screen
def welcome_screen():
    print(GREEN + BRIGHT + r"""
╔╗─╔╦═══╦═══╗╔═══╗────╔╗
║║─║║╔═╗╠╗╔╗║║╔═╗║────║║
║║─║║║─╚╝║║║║║║─║╠╦═╦═╝╠═╦══╦══╗
║║─║║║╔═╗║║║║║╚═╝╠╣╔╣╔╗║╔╣╔╗║╔╗║
║╚═╝║╚╩═╠╝╚╝║║╔═╗║║║║╚╝║║║╚╝║╚╝║
╚═══╩═══╩═══╝╚╝─╚╩╩╝╚══╩╝╚══╣╔═╝
────────────────────────────║║
────────────────────────────╚╝
""")
    print(YELLOW + BRIGHT + "Channel: https://t.me/UGDairdrop\n".center(80))
    for _ in range(3):
        print(BLUE + "Loading" + "." * (_ + 1))
        time.sleep(0.5)
    print()

async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            uri = "wss://proxy.wynd.network:4650/"
            server_hostname = "proxy.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)
            async with proxy_connect(
                uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname, extra_headers=custom_headers
            ) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}}
                        )
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(20)

                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "2.5.0"
                            }
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)
            logger.error(socks5_proxy)

async def fetch_proxies_periodically(interval, user_id):
    while True:
        print(CYAN + BRIGHT + "Pilih URL proxy:")
        print("1. Proxifly (All)")
        print("2. Yakumo (PMix Checked)")
        print("3. Yakumo (GRASS GOOD)")
        print("4. Yakumo (Socks5 Global)")
        print("5. Yakumo (HTTP Global)")
        print("6. Monosans (All)")
        choice = input("Pilih URL proxy (1-6): ")

        if choice == '1':
            proxy_url_choice = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"
        elif choice == '2':
            proxy_url_choice = "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/pmix_checked.txt"
        elif choice == '3':
            proxy_url_choice = "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/GRASS_GOOD.txt"
        elif choice == '4':
            proxy_url_choice = "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/psocks5_checked.txt"
        elif choice == '5':
            proxy_url_choice = "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/http/global/phttp_checked.txt"
        elif choice == '6':
            proxy_url_choice = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"
        else:
            print(RED + "Pilihan tidak valid.")
            continue

        socks5_proxy_list = fetch_proxies(proxy_url_choice)
        tasks = [asyncio.ensure_future(connect_to_wss(i, user_id)) for i in socks5_proxy_list]
        await asyncio.gather(*tasks)
        await asyncio.sleep(interval)

async def main(interval):
    welcome_screen()
    user_id = input(MAGENTA + "Masukkan User ID: ")
    loading_task = asyncio.create_task(asyncio.to_thread(animated_loading, "Fetching proxies "))
    await fetch_proxies_periodically(interval, user_id)
    loading_task.cancel()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WebSocket proxy connection script')
    parser.add_argument('--interval', type=int, default=1800, help='Interval to fetch proxies (in seconds)')
    args = parser.parse_args()

    asyncio.run(main(args.interval))
