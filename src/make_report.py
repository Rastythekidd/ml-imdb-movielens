"""Prosty raport po polsku. Wyniki są odczytywane z plików wynikowych."""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
from xml.sax.saxutils import escape
from urllib.parse import urlsplit
import argparse,csv,json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from analysis import setup_fonts
ROOT=Path(__file__).resolve().parents[1]
STYLE={
 'tytul':ParagraphStyle('tytul',fontName='ProjectBold',fontSize=20,leading=25,spaceAfter=14),
 'naglowek':ParagraphStyle('naglowek',fontName='ProjectBold',fontSize=15,leading=20,spaceAfter=12),
 'podtytul':ParagraphStyle('podtytul',fontName='ProjectBold',fontSize=11,leading=15,spaceBefore=9,spaceAfter=5),
 'tekst':ParagraphStyle('tekst',fontName='Project',fontSize=10.5,leading=14.7,spaceAfter=8),
 'maly':ParagraphStyle('maly',fontName='Project',fontSize=8.7,leading=12,spaceAfter=6),
 'komorka':ParagraphStyle('komorka',fontName='Project',fontSize=9,leading=12),
 'komorka_naglowek':ParagraphStyle('komorka_naglowek',fontName='ProjectBold',fontSize=9,leading=12)}
def p(s,styl='tekst'):return Paragraph(s,STYLE[styl])
def f(v,n=2):return f'{v:.{n}f}'.replace('.',',')
def tabela(wiersze,szerokosci):
 dane=[[p(escape(str(x)),'komorka_naglowek' if i==0 else 'komorka') for x in r] for i,r in enumerate(wiersze)]
 t=Table(dane,colWidths=szerokosci,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#ECEFF1')),
  ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
  ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
  ('LINEBELOW',(0,0),(-1,0),.7,colors.black),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#999999'))]))
 return t
def wykres(nazwa,wys=215):
 return Image(str(ROOT/'results/figures'/f'{nazwa}.png'),width=wys*520/300,height=wys,hAlign='CENTER')
def stopka(c,doc):
 c.setFont('Project',8);c.setFillColor(colors.HexColor('#555555'))
 c.drawString(48,26,'Uczenie maszynowe - projekt 1, etap pierwszy')
 c.drawRightString(A4[0]-48,26,str(doc.page))
def link(url):return '<link href="'+escape(url)+'" color="#174B78">'+escape(url)+'</link>'
def main():
 ap=argparse.ArgumentParser(description='Tworzenie raportu pierwszego etapu.')
 ap.add_argument('--repo-url',help='Adres repozytorium, np. https://github.com/OWNER/REPO')
 args=ap.parse_args();setup_fonts()
 m=json.loads((ROOT/'project.json').read_text(encoding='utf-8'))
 s=json.loads((ROOT/'results/summary.json').read_text(encoding='utf-8'))
 repo=args.repo_url or m.get('repository_url')
 if repo:
  u=urlsplit(repo)
  if u.scheme!='https' or u.netloc.lower()!='github.com' or len([x for x in u.path.split('/') if x])!=2:
   raise ValueError('Podaj adres repozytorium GitHub z nazwą konta i repozytorium. Sam profil nie wystarcza.')
 if args.repo_url:
  m['repository_url']=repo;(ROOT/'project.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
 ml=s['movielens'];im=s['imdb'];neg=im['word_counts']['negatywny'];pos=im['word_counts']['pozytywny']
 with (ROOT/'results/word_frequencies.csv').open(encoding='utf-8-sig',newline='') as file:
  slowa={(r['sentiment'],r['word']):int(r['documents']) for r in csv.DictReader(file)}
 tresc=[]
 def dodaj(*x):tresc.extend(x)
 def strona(tytul):dodaj(PageBreak(),p(tytul,'naglowek'))

 dodaj(p('Uczenie maszynowe<br/>Projekt 1 - etap pierwszy','tytul'),
  p('Temat: analiza recenzji IMDb i ocen filmów MovieLens','podtytul'),
  p('Data opracowania: '+m['date'],'maly'),
  tabela([['Osoba','Nr indeksu','Podział odpowiedzialności']]+[[r['name'],r['id'],r['role']] for r in m['team']],[138,64,297]),
  Spacer(1,12),p('1. Cel projektu','naglowek'),
  p('W projekcie analizujemy dwa rodzaje opinii: tekstowe recenzje z IMDb i liczbowe oceny z MovieLens. Chcemy opisać dane, znaleźć widoczne zależności oraz przygotować pytania do dalszej pracy z modelami uczenia maszynowego.'),
  p('Pytania badawcze','podtytul'),
  p('1. Czy pozytywne i negatywne recenzje różnią się długością i używanymi słowami?<br/>'
    '2. Jak rozkładają się oceny MovieLens i jaki mają związek z rokiem premiery?<br/>'
    '3. Czy w kolejnym etapie uda się rozpoznawać sentyment recenzji lepiej niż prostą metodą bazową?'),
  p('Wykorzystane dane','podtytul'),
  p('Mamy 200 recenzji IMDb oraz 200 ocen MovieLens. Plik MovieLens_filmy zawiera te same oceny co MovieLens_liczby, ale z nazwami filmów. Są to dwa zbiory danych, mimo że zapisano je w trzech plikach Excel.'),
  p('Jedna recenzja nie jest tym samym co jeden film, a jedna ocena MovieLens oznacza opinię konkretnego użytkownika o konkretnym filmie. Nie łączymy IMDb i MovieLens według numerów wierszy.'),
  p('Na tym etapie wykonaliśmy analizę danych i kontrolę ich poprawności. Uczenie modeli oraz interfejs z predykcjami należą do kolejnego etapu.','maly'))

 strona('2. Źródła i przygotowanie danych')
 dodaj(p('IMDb','podtytul'),
  p('Recenzje pochodzą z Large Movie Review Dataset v1.0 (Maas i in., 2011), udostępnionego również jako stanfordnlp/imdb na Hugging Face. Z części train wybrano po 100 recenzji negatywnych i pozytywnych. Użyto jednego generatora random.Random(42): najpierw losowanie w klasie 0, potem w klasie 1, a następnie przetasowanie indeksów.'),
  p('Nazwy i identyfikatory tytułów ustalono na podstawie oryginalnego archiwum recenzji oraz metadanych IMDb pobranych 25.10.2026. Podczas przygotowania danych 11 recenzji zastąpiono innymi prawdziwymi recenzjami tej samej klasy, ponieważ ich pierwotnych ID nie znaleziono w pobranych metadanych. Wykaz zmian i końcowe pliki źródłowe zapisano w manifeście.'),
  p('Etykiety pochodzą ze źródła: negatywna recenzja ma oryginalną ocenę do 4/10, a pozytywna od 7/10. W tym zbiorze nie ma klasy neutralnej. Równowaga 100/100 jest wynikiem doboru danych.'),
  p('MovieLens','podtytul'),
  p('Zbiór MovieLens 100K zawiera 100 000 ocen od 943 użytkowników dla 1682 filmów. Wybrano 200 rekordów z u.data poleceniem random.Random(42).sample(range(100000), 200). Rok premiery i nazwę filmu dołączono z u.item według ID filmu. Są to historyczne dane z lat 1997-1998.'),
  p('Znaczenie kolumn','podtytul'),
  tabela([['Plik / kolumny','Znaczenie'],
   ['IMDb: tytul_filmu, id_imdb, link_imdb','Nazwa tytułu, jego identyfikator i link do strony IMDb.'],
   ['IMDb: tekst_recenzji, sentyment','Oryginalny tekst angielski oraz etykieta: pozytywny albo negatywny.'],
   ['MovieLens: id_uzytkownika, id_filmu','Identyfikatory użytkownika i filmu. Ich wartości nie oznaczają wielkości cechy.'],
   ['MovieLens: ocena','Ocena użytkownika w skali od 1 do 5.'],
   ['MovieLens: czas_unix','Czas wystawienia oceny w sekundach od 01.01.1970, UTC.'],
   ['MovieLens: rok_premiery','Rok premiery, odrębny od daty wystawienia oceny.']],[220,279]),
  Spacer(1,9),p('Oryginalne pliki Excel zachowano bez zmian. Do analizy tekstu usunięto znaczniki HTML, zdekodowano encje i ujednolicono odstępy. Liczbę słów zmierzono przed pomijaniem stopwords. Przy analizie słownictwa zachowano przeczenia, np. not.','maly'),
  p('Dane przygotowano 25.10.2026. Pełną kontrolę powtórzono 27.10.2026. Dokładną kolejność rekordów, hashe i pochodzenie każdej recenzji zapisano w sources/source_manifest.json.','maly'))

 strona('3. Analiza ocen MovieLens')
 dodaj(tabela([['Miara','Wynik'],
  ['Liczba ocen / filmów / użytkowników',f'{ml["n"]} / {ml["unique_movies"]} / {ml["unique_users"]}'],
  ['Średnia / mediana',f'{f(ml["rating_summary"]["mean"])} / {f(ml["rating_summary"]["median"],0)}'],
  ['Odchylenie standardowe',f(ml['rating_summary']['std_sample'])],
  ['Oceny 4 i 5','98 z 200, czyli 49,0%']],[275,224]),
  Spacer(1,7),wykres('03_rating_distribution',205),
  p('Najczęstsza ocena to 3: występuje 59 razy, czyli w 29,5% rekordów. Średnia 3,42 opisuje wybrane oceny użytkowników, a nie średnią po wszystkich filmach.','maly'),
  wykres('05_year_rating',205),
  p(f'Współczynnik korelacji rang Spearmana między rokiem premiery a oceną wynosi {f(ml["spearman_year_rating"],3)}. W próbie zależność jest słaba i ujemna. Po uśrednieniu ocen dla każdego filmu wynosi {f(ml["spearman_year_film_mean"],3)}. Nie jest to dowód, że starsze filmy są lepsze.'),
  p('Aż 150 filmów ma w próbie tylko jedną ocenę. Użytkownicy i filmy powtarzają się, dlatego zależność opisujemy bez testu istotności zakładającego niezależność wszystkich wierszy. 141 ocen dotyczy filmów z lat 90.; najpóźniejsza premiera to 1998 r.','maly'))

 strona('4. Analiza recenzji IMDb')
 dodaj(tabela([['Miara','Negatywne','Pozytywne'],
  ['Liczba recenzji','100','100'],
  ['Średnia liczba słów',f(neg['mean']),f(pos['mean'])],
  ['Mediana liczby słów',f(neg['median'],1),f(pos['median'],1)],
  ['Odchylenie standardowe',f(neg['std_sample']),f(pos['std_sample'])],
  ['Minimum / maksimum',f(neg['min'],0)+' / '+f(neg['max'],0),f(pos['min'],0)+' / '+f(pos['max'],0)]],[219,140,140]),
  Spacer(1,7),wykres('02_review_length',225),
  p('Pozytywne recenzje mają większą średnią długość, ale mniejszą medianę. Długie teksty wpływają na średnią, a oba rozkłady mocno się nakładają. Sama długość nie wystarcza więc do pewnego rozpoznania sentymentu.'),
  p('Przykładowe słowa w obu klasach','podtytul'),
  tabela([['Słowo','Recenzje negatywne','Recenzje pozytywne']]+[
   [word,slowa.get(('negatywny',word),0),slowa.get(('pozytywny',word),0)] for word in ['bad','great','good','not']],[139,180,180]),
  p('Tabela pokazuje liczbę recenzji zawierających słowo, najwyżej raz na recenzję. Słowa good i not pojawiają się w obu klasach, dlatego przy dalszej klasyfikacji trzeba uwzględnić kontekst.','maly'),
  p('200 recenzji dotyczy 189 tytułów. Według metadanych 167 recenzji dotyczy typu movie, a 33 innych typów, np. filmów telewizyjnych i seriali; jedna dotyczy typu videoGame. Zachowano zebraną próbę i opisano ten zakres zamiast usuwać rekordy po analizie.','maly'))

 strona('5. Kontrola, wnioski i dalsza praca')
 dodaj(p('Kontrola poprawności','podtytul'),
  p('Sprawdzono wszystkie 200 recenzji i 200 ocen oraz zgodność obu plików MovieLens. Nie znaleziono braków ani powtórzonych pełnych wierszy. Teksty, etykiety, oceny i ID porównano z archiwami źródłowymi. Nazwy 189 tytułów potwierdzono w zapisanym pliku metadanych IMDb. Nie było potrzeby zmiany wartości w arkuszach.'),
  p('Wnioski','podtytul'),
  p('1. Długość recenzji różni się opisowo między klasami, ale rozkłady nakładają się. Widać też różnice słownictwa.<br/>'
    '2. W MovieLens dominują oceny 3-5. Związek oceny z rokiem premiery jest słaby.<br/>'
    '3. Skuteczność automatycznego rozpoznawania sentymentu sprawdzimy dopiero podczas uczenia modeli.'),
  p('Próby po 200 rekordów są małe. IMDb dobrano celowo po 100 rekordów każdej klasy, a 11 rekordów zastąpiono według dostępności metadanych. Wyników nie traktujemy jako opinii wszystkich widzów. Zbiory IMDb i MovieLens analizujemy osobno.'),
  p('Linki i odtwarzanie','podtytul'),
  p('Kontrola adresów jest w results/kontrola_linkow.json. IMDb ogranicza automatyczny dostęp, dlatego odpowiedzi 202/403 nie oznaczają usunięcia tytułów. Jeden adres w oryginalnym tekście recenzji (B91) zwraca 404; nie zmieniono autentycznej recenzji. Część źródeł była niedostępna z powodu błędów połączenia lub certyfikatu.'),
  p('Instrukcja uruchomienia znajduje się w README.md. Wyniki można odtworzyć poleceniem python src/run_all.py. Archiwa do kontroli offline są w data/raw; do zwykłego przeliczenia analizy wystarczą trzy arkusze.','maly'),
  p('Repozytorium GitHub: '+(link(repo) if repo else '<b>adres do uzupełnienia po utworzeniu repozytorium przez zespół.</b>'),'maly'),
  p('Źródła','podtytul'),
  p('[1] Maas A. L. i in. (2011), Learning Word Vectors for Sentiment Analysis, ACL, s. 142-150. '+link('https://aclanthology.org/P11-1015/'),'maly'),
  p('[2] Dane IMDb: '+link('https://huggingface.co/datasets/stanfordnlp/imdb')+'. Źródło pierwotne: '+link('https://ai.stanford.edu/~amaas/data/sentiment/'),'maly'),
  p('[3] MovieLens 100K: '+link('https://grouplens.org/datasets/movielens/100k/')+'. Harper F. M., Konstan J. A. (2015), The MovieLens Datasets: History and Context, ACM TiiS 5(4), art. 19. DOI: 10.1145/2827872.','maly'),
  p('[4] Metadane IMDb: '+link('https://developer.imdb.com/non-commercial-datasets/')+'. Zapis wykorzystany w projekcie: 25.10.2026.','maly'))
 target=ROOT/Path(m.get('report_file','Raport_etap_1.pdf')).name
 doc=SimpleDocTemplate(str(target),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=47,bottomMargin=44,
  title=m['title'],author='; '.join(r['name'] for r in m['team']),subject='Projekt 1 - etap pierwszy')
 doc.build(tresc,onFirstPage=stopka,onLaterPages=stopka)
 print('Zapisano raport:',target)
if __name__=='__main__':main()
