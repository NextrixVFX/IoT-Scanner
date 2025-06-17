from colorama import Fore
from threading import Thread
from datetime import date

from src.Database import Database
from src.Generator import Generator
from src.Checker import Checker

class IoTScanner:
    def __init__(self, timeout: float = .5, threads: int = 1, ips: int = 10_000, ports: tuple[int] = (80, 21)) -> None:
        self.timeout: float = timeout
        self.threads: int = threads
        self.ips: int = ips
        self.ports: tuple[int] = ports

        # Instances
        self.gen: Generator = Generator()
        self.db: Database = Database(f"data\\{date.today()}.txt")


    def main(self) -> set[str]:
        threadList: list[Thread] = []

        for threadNum in range(self.threads):
            ipSet: set[str] = self.gen.generateIPs(self.ips)

            # Timeout is determined on network speed, also timeout = timeout / length(ports)
            checker: Checker = Checker(self.db, ipSet, self.timeout, writeToFS=True)
            
            threadList.append(Thread(target=checker.portCheck, args=(self.ports, threadNum)))
            threadList[threadNum].start()
        
        # wait for threads to finish
        for threadNum in range(self.threads):
            threadList[threadNum].join()
            print(f"{Fore.BLUE}[!] Thread {threadNum+1} Finished!{Fore.RESET}")
        
        # Due to threading; one thread might find the same ip as another thread.
        return self.db.removeDuplicates(writeToFS=True)

if __name__ == "__main__":
    ports: tuple[int] = (80, 554, 67, 23, 9000)
    iotScanner: IoTScanner = IoTScanner(timeout=.35, threads=3, ips=10_000, ports=ports)
    validIPs: set[str] = iotScanner.main()
