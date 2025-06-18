from scapy.all import IP, TCP, sr1
from colorama import Fore

from src.Database import Database

class Checker:
    def __init__(self, db: Database, ipList: set[str], timeout: float, writeToFS: bool = True) -> None:
        self.db: Database = db
        self.ipList: set[str] = ipList
        self.timeout: float = timeout
        self.writable: bool = writeToFS    

    # Returns valid ips
    def portCheck(self, ports: tuple[int], threadNum: int = -1) -> set[str]:
        threadStr: str = f"[MT : {threadNum+1}]" if threadNum+1 else "[NT]"
        validIPs: set[str] = set()
        for i, ip in enumerate(self.ipList, 1):
            for port in ports:
                packet = IP(dst=ip) / TCP(dport=port, flags='S')
                res = sr1(packet, timeout=self.timeout / len(ports), verbose=0)

                if res is None or not res.haslayer(TCP):
                    print(f"{threadStr} {Fore.BLUE}[{i}] {ip} is Invalid...{Fore.RESET}")
                    break

                if res[TCP].flags == "SA":  # SYN-ACK received
                    print(f"{threadStr} {Fore.GREEN}[+] Port {port} is OPEN on {ip}{Fore.RESET}")
                    validIPs.add(f"{ip}:{port}")
                    
                    if self.writable:
                        self.db.writeData(f"{ip}:{port}\n")

                elif res[TCP].flags == "RA":
                    print(f"{threadStr} {Fore.RED}[-] Port {port} is CLOSED on {ip}{Fore.RESET}")

        return validIPs
    
if __name__ == "__main__":
    exit(0)
