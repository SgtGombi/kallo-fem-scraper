"""
Leírás:
CMD-ben futtatással ellenőrzi hogy a kérdéses .JSON fájlban van-e duplikátum.
A webshop felépítéséből adódóan (nincsennek összefonódó oldalak, sem duplikátum
- kivéve ha nem ?page=1 használat van -, így nincs szükség a spiderben
duplikátum ellenőrzésre minden futtatás során, így ez a kód biztonsági ellenőrzés
esetére jött létre

Jellemzők:
Egyedi azonosító a név, azt hasonlítja össze az elemek között, kigyűjti a duplikátumot.

Futtatás (a .py fájl egy helyen van a .json fájllal):
cd \gyökérkönyvtár
python check_duplicates.py fajlneve.json
"""

import json
from collections import defaultdict

def check_duplicates(json_file): # Bemenetbe várja a .JSON fájlt, és megnyitja/betölti
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    name_counts = defaultdict(list) #kulcsnak a kisbetűs/szóközmentes terméknév
    for idx, item in enumerate(data):
        if 'Terméknév' in item and item['Terméknév']:
            name = item['Terméknév'].strip().lower()
            name_counts[name].append(idx + 1) #+1 az indexre emberi olvasás segítéséhez

    # duplicates tömb: ide gyűjti azokat az elemeket, ahol a név megegyezik
    duplicates = {name: lines for name, lines in name_counts.items() if len(lines) > 1}

    # if duplicates: ha van benne érték, tehát igaz, akkor kiírja a kért módon a duplikációt
    if duplicates:
        print(f"{len(duplicates)} duplikátum található a fájlban!")
        for name, lines in duplicates.items():
            print(f"  - '{name}': sorok {lines}")
    # más esetben pedig a megerősítést hogy nincs
    else:
        print("Nincsenek duplikátumok a fájlban!")

# Közvetlen futtatáskor fut le, az alábbi kódrész
if __name__ == "__main__":
    import sys

    # Ha nincs 2 argumentum (checkduplicates.py fajlnev.json hibaüzenetet dob
    if len(sys.argv) != 2:
        print("Használat: python checkduplicates.py <json_fájl>")
        sys.exit(1)

    json_file = sys.argv[1] #A második argumentum maga a .JSON fájl, amire futtatja a check_duplicates fv-t.
    try:
        check_duplicates(json_file) # meghívja a függvényt az argumentumban megadott .JSON fáljra
    except FileNotFoundError: # Kivételkezelés
        print(f"A fájl nem található: {json_file}") # HIBAÜZENET ha nincs/érvénytelen a .JSON file.
    except json.JSONDecodeError:
        print(f"Érvénytelen JSON fájl: {json_file}")