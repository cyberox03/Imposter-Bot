import nmap
import time
from getmac import get_mac_address
from telegram import Bot
from telegram.constants import ParseMode
import asyncio

# Configuration
IP = '192.168.175.202' #you can specify you wifi or hotpot device' IP
KNOWN_DEVICES = []
TELEGRAM_BOT_TOKEN = '7559303386:AAFe_HrEHzaXdBTctasH2bj4K3aIcHM7rbs' # specify your telegram bot's token (you can get it ftom BotFather)
CHAT_ID = '-4666596018' # specify your group's chat id

class NetworkScanner:

    def __init__(self, ip: str):
        self.ip = ip
        self.connected_devices = set()
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)

        # Specify Nmap path
        self.nmap_path = "C:\\Program Files (x86)\\Nmap\\nmap.exe"

    async def scan(self):
        """ Continuously scans the network for new devices. """
        network = f"{self.ip}/24"
        nm = nmap.PortScanner(nmap_search_path=(self.nmap_path,))

        while True:
            try:
                # Run the Nmap scan
                nm.scan(hosts=network, arguments='-sn')

                # Check if output is empty
                if not nm.all_hosts():
                    print("⚠️ No devices found or empty result!")
                    time.sleep(10)
                    continue

                # Iterate through hosts
                for host in nm.all_hosts():
                    mac = get_mac_address(ip=host)
                    if mac:
                        print(f"Device Found: {mac}")

                    # Notify only for new, unknown devices
                    if mac and mac not in self.connected_devices and mac not in KNOWN_DEVICES:
                        print('New Device Found!')
                        await self.notify_new_device(mac)
                        self.connected_devices.add(mac)

                time.sleep(10)  # Delay between scans

            except Exception as e:
                print(f"⚠️ Error occurred: {e}")
                time.sleep(10)

    async def notify_new_device(self, mac):
        """ Sends a Telegram message for new devices. """
        message = f"🚨 *New Device Connected!* 🚨\n\n📡 *MAC Address:* `{mac}`"
        await self.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )

async def main():
    scanner = NetworkScanner(IP)
    await scanner.scan()

# Run the async event loop
if __name__ == '__main__':
    asyncio.run(main())
