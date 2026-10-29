"""Zapis czytelnej tabeli z kontroli adresów. Nie zmienia danych źródłowych."""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    dane=json.loads((ROOT/'results/kontrola_linkow.json').read_text(encoding='utf-8'))
    with (ROOT/'results/kontrola_linkow.csv').open('w',encoding='utf-8-sig',newline='') as plik:
        pola=['adres','status','kod_http','adres_koncowy','uwaga']
        w=csv.DictWriter(plik,fieldnames=pola);w.writeheader()
        for r in dane['wyniki']:
            w.writerow({'adres':r['url'],'status':r['status'],'kod_http':r.get('kod_http',''),
                'adres_koncowy':r.get('adres_koncowy',''),'uwaga':r.get('blad','')})
    print('Zapisano tabelę kontroli',len(dane['wyniki']),'adresów.')
if __name__=='__main__':main()
