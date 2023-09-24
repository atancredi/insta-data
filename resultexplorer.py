from os import listdir
from os.path import splitext
from data import Scan
from typing import List

def scan_folder() -> List[Scan]:
    results = []
    for file in listdir("results"):
        name,ext = splitext(file)
        if "json" in ext.lower():
            s = Scan(file)
            results.append(s)
    return results

if __name__ == "__main__":
    for result in scan_folder():
        print(result.date.to_string())