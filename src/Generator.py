from colorama import Fore
from random import randint

class Generator:
    def __init__(self) -> None:
        pass

    def generateIPs(self, count: int) -> set[str]:
        ipList: set[str] = set()
        
        while len(ipList) < count:
            octets: list[int] = [randint(1, 255) for _ in range(4)]
            ip: str = f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}"

            if not (ip.startswith("10.") or
                    ip.startswith("192.168.") or
                    ip.startswith("172.") and 16 <= octets[1] <= 31 or
                    ip.startswith("127.") or
                    octets[0] >= 224):  # Multicast/reserved
                if ip not in ipList: ipList.add(ip)

        print(f"{Fore.YELLOW}Generated {count:,} IP's{Fore.RESET}\n")
        return ipList
    
if __name__ == "__main__":
    exit(0)