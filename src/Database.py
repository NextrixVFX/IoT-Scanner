from typing import TextIO
from colorama import Fore

class Database:
    def __init__(self, outputName: str) -> None:
        self.outputName: str = outputName
        
        try:
            self.fs: TextIO = open(self.outputName, 'a')
        except:
            print(f"File at path: {self.outputName} doesn't exist.")
            exit(0)

    def writeData(self, data: str) -> None:
        self.fs.write(data)

        if not self.fs.closed:
            self.fs.flush()

    def removeDuplicates(self, writeToFS: bool = False) -> set[str]:
        seenLines: set[str] = set()

        with open(self.outputName, 'r') as readFS:
            for line in readFS.readlines():
                if line not in seenLines:
                    seenLines.add(line)
            
            readFS.close()

        debug: str = f"{Fore.YELLOW}[*] Removed Duplicates"

        if writeToFS:
            with open(self.outputName, 'w') as writeFS:
                writeFS.writelines(list(seenLines))
                writeFS.close()
                debug += f" and saved to {self.outputName}."


        print(debug + Fore.RESET)
        return seenLines
    
    def closeFS(self) -> None:
        if not self.fs.closed:
            self.fs.close()

if __name__ == "__main__":
    exit(0)