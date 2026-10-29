# Projekt 1 — analiza recenzji IMDb i ocen MovieLens

Przedmiot: Uczenie maszynowe. Etap pierwszy: dane, analiza i pytania badawcze.
Podzbiory przygotowano 25.10.2026. Kontrolę i analizę powtórzono 27.10.2026.

## Zespół
- Andrei Rastsiahayeu — 71629
- Vadym Karkhut — 71513
- Yulia Khrystonko — 72072
- Kateryna Ivanchenko — 72646
- Alisa Kosenkova — 71510

Podział odpowiedzialności jest w raporcie i project.json. Profil koordynatora: https://github.com/Rastythekidd.
Repozytorium projektu: https://github.com/Rastythekidd/ml-imdb-movielens

## Od czego zacząć
1. Otwórz Raport_etap_1_z_linkiem.pdf — uproszczony raport na 5 stron.
2. Przeczytaj OPIS_PROJEKTU.md — wyjaśnienie każdej części i przygotowanie do omówienia projektu.
3. KONTROLA.md opisuje kontrolę danych i sprawdzenie adresów.
4. results/figures zawiera siedem wykresów w PNG i PDF.

## Jakie dane mamy
- data/original/IMDb_recenzje.xlsx — 200 angielskich recenzji, po 100 na klasę.
- data/original/MovieLens_liczby.xlsx — 200 ocen użytkownik-film, tylko pola liczbowe.
- data/original/MovieLens_filmy.xlsx — te same 200 ocen z nazwami filmów.

To dwa zbiory, zapisane w trzech plikach. Nie łączymy wierszy IMDb i MovieLens według pozycji.
Oryginalne arkusze nie zostały zmienione. Teksty angielskie zachowano w języku źródła.

## Uruchomienie
Wymagany Python 3.11 lub nowszy. Wykonanie sprawdzono na Pythonie 3.12.
Polecenia uruchamiaj w folderze Project:

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt
    python src/run_all.py

Na Linux aktywacja środowiska: source .venv/bin/activate.
Raport wymaga Arial na Windows albo DejaVu Sans na Linux. Na innym systemie dostosuj ścieżki w setup_fonts() w src/analysis.py.

Oddzielne kroki:

    python src/analysis.py
    python src/render_figures.py
    python src/make_report.py

Nie uruchamiaj z opcją python -O, ponieważ walidacja wykorzystuje assert.
Gotowy raport i wykresy można oglądać bez uruchamiania kodu.
Notebook Analiza_etap_1.ipynb uruchamia ten sam kod. Wymaga dodatkowo Jupyter lub rozszerzenia Jupyter w VS Code.

## Pełna kontrola źródeł
W folderze data/raw są cztery zachowane pliki: aclImdb_v1.tar.gz, ml-100k.zip, imdb_train.parquet i title.basics.tsv.gz.
Nie są potrzebne do zwykłej analizy, ale umożliwiają kontrolę offline.

    python src/kontrola_danych.py
    python src/reproduce_subset.py --raw-dir data/raw --out-dir _robocze/odtworzone

Pierwsza komenda sprawdza wszystkie wartości w danych. Druga odtwarza wybrane wiersze jako CSV i porównuje je z oryginałami.
Skrypty nie zapisują zmian w XLSX.

W archiwum Projekt_etap_1_z_linkiem.zip pominięto duże data/raw oraz pliki robocze. Jeżeli korzystasz tylko z ZIP, pobierz źródła:

    python src/reproduce_subset.py --download

Pobieranie Stanford/GroupLens może zależeć od dostępności serwerów i poprawnego zestawu certyfikatów na komputerze.
Podczas tej kontroli nie udało się potwierdzić pobierania z obu serwerów; dlatego w lokalnym Project zachowano archiwa.
Nie wyłączaj weryfikacji HTTPS. Po pobraniu skrypt kontroluje SHA-256.

## Co jest w pozostałych folderach
- src — kod analizy, raportu, odtwarzania i kontroli.
- sources — manifest pochodzenia oraz oryginalne dokumenty README źródeł.
- results — statystyki, częstości słów i kontrole.
- data/derived — obliczone cechy recenzji oraz czytelne daty ocen.
- _robocze — podglądy raportu, logi i kontrola odtworzenia; nie są częścią oddawanego raportu.

Wyniki w summary.json używają stałych nazw technicznych. Słownik kolumn i definicje podano w raporcie i OPIS_PROJEKTU.md.

## Źródła i dobór
IMDb: https://huggingface.co/datasets/stanfordnlp/imdb
Źródło pierwotne: https://ai.stanford.edu/~amaas/data/sentiment/
Część train, plik plain_text/train-00000-of-00001.parquet.
Jeden random.Random(42): po 100 indeksów klas 0 i 1, potem shuffle.
11 rekordów zastąpiono w tych samych klasach z powodu dostępności metadanych. Nie jest to końcowo prosta próba losowa.

MovieLens 100K: https://grouplens.org/datasets/movielens/100k/
random.Random(42).sample(range(100000), 200) z u.data. Nazwy i lata z u.item.

Nazwy IMDb: snapshot title.basics.tsv.gz z 25.10.2026.
https://developer.imdb.com/non-commercial-datasets/

Manifest sources/source_manifest.json zawiera dokładną kolejność wierszy, oryginalne pliki recenzji, indeksy, 11 zamian i sumy kontrolne.
Nazwy tytułów są odtwarzane ze snapshotu w manifeście, ponieważ publiczne metadane zmieniają się codziennie.

## Definicje obliczeń
- Długość: tokeny z liter angielskich i opcjonalnego apostrofu; po usunięciu HTML i dekodowaniu encji.
- Długość liczona przed pominięciem stopwords.
- Słownictwo: minimum 3 znaki, jawna lista results/stopwords.txt; zachowano przeczenia.
- Częstość dokumentowa: jedno słowo liczy się najwyżej raz w jednej recenzji.
- Kwartyle: interpolacja liniowa; odchylenie standardowe: n-1.
- Spearman: korelacja rang ze średnimi rangami przy remisach.
- Nie wykonano testu istotności ignorującego zależność wierszy od użytkownika lub filmu.
- Przesunięcie punktów na wykresie nie zmienia danych obliczeń.
- Wszystkie wyniki dotyczą dostarczonych podzbiorów.

## GitHub i oddanie
Adres repozytorium został dodany do raportu. Pliki do repozytorium przesyła zespół. Aby ponownie wygenerować raport z tym adresem:

    python src/make_report.py --repo-url https://github.com/Rastythekidd/ml-imdb-movielens

Komenda aktualizuje project.json i tworzy nowy Raport_etap_1_z_linkiem.pdf. Sam adres profilu GitHub nie wystarcza.
Do Platona, zakładka „projekt”, wyślij jeden nowy PDF.

README MovieLens ogranicza redystrybucję danych. .gitignore pomija dane i część tabel z tytułami w publikacji przez Git.
Przy wysyłaniu przez stronę GitHub wybieraj pliki świadomie: .gitignore nie filtruje ręcznego wyboru.
Zgodność udostępniania samych danych z warunkami źródła i wymaganiami prowadzącego trzeba ustalić przed publikacją.

Instrukcja zawiera dwa terminy: 30.10.2026 23:59 oraz 31.10.2026 23:59. Przyjmij wcześniejszy i sprawdź ogłoszenie.
Modele nadzorowane, bez nadzoru, transformery i interfejs z predykcjami należą do dalszej pracy.

## Końcowa kontrola całego projektu

Przy obecnych lokalnych archiwach: python src/sprawdz_projekt.py. Skrypt porównuje obliczenia, odtwarza dane bez XLSX i sprawdza raport. Wynik jest w results/verification.json.

Aktualny raport: Raport_etap_1_z_linkiem.pdf. Starszy Raport_etap_1.pdf nie zawiera adresu repozytorium i nie jest wersją do oddania.
