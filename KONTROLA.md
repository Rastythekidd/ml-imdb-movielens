# Kontrola danych i adresów — 27.10.2026

## Wynik kontroli danych
Sprawdzono 200 recenzji IMDb i 200 ocen MovieLens. Drugi arkusz MovieLens jest widokiem tych samych ocen, nie kolejnymi 200 obserwacjami.
Nie wykryto błędnych wartości, braków, duplikatów pełnych wierszy ani formuł w danych.
Nie zmieniono wartości ani formatowania oryginalnych plików XLSX.

Każdy tekst i jego etykietę porównano z oryginalnym plikiem train/pos lub train/neg. Potwierdzono źródłowy ID z plików urls_pos.txt i urls_neg.txt.
Każdą ocenę, użytkownika, film, czas i rok premiery porównano z u.data oraz u.item.
Nazwy i typy 189 tytułów potwierdzono w zapisanym snapshotcie title.basics.tsv.gz.

Wynik jest zapisany w results/kontrola_danych_szczegolowa.json.
Kontrolę można powtórzyć offline: python src/kontrola_danych.py.

## Rzeczy, które trzeba poprawnie opisać
- IMDb: 100 recenzji pozytywnych i 100 negatywnych dobrano celowo, nie jest to naturalny rozkład opinii.
- 11 recenzji zastąpiono podczas przygotowania nazw tytułów. Wszystkie zmiany są jawne w manifeście.
- 167 recenzji dotyczy typu movie, a 33 innych typów. Nie wolno nazywać wszystkich rekordów recenzjami pełnometrażowych filmów.
- MovieLens: 172 filmy i 161 użytkowników, mimo 200 wierszy.
- Braków i duplikatów nie usuwano, ponieważ ich nie stwierdzono.
- Nie łączono danych obu serwisów po numerze wiersza.

## Wynik sprawdzenia linków
Wykonano żądania do 399 różnych adresów znalezionych w danych, dokumentacji i raporcie oraz do wskazanego profilu GitHub.

- 10 adresów zwróciło poprawną odpowiedź.
- 380 adresów blokowało automatyczną kontrolę — głównie strony IMDb i przekierowania DOI.
- 8 adresów nie udało się potwierdzić z powodu timeoutu lub problemu z certyfikatem.
- 1 adres zwracał 404.
- 2 szablony/fragmenty URL odnotowano osobno; nie traktowano ich jako prawdziwych adresów.

HTTP 202/403 nie dowodzi, że film zniknął. Nie oznaczono tych stron jako działające ani jako usunięte.
Weryfikacja danych w archiwach jest niezależna od bieżącej dostępności stron internetowych.

Niedostępny adres:
http://www.cinemablend.com/forum/showthread.php?s=&threadid=21699
Jest częścią angielskiej recenzji w IMDb_recenzje.xlsx, komórka B91. Pozostawiono oryginalny tekst, aby nie fałszować źródła.

Podczas dodatkowej kontroli potwierdzono:
- stronę stanfordnlp/imdb na Hugging Face (HTTP 200),
- źródłowy plik Parquet na Hugging Face (HTTP 206),
- istnienie publikacji MovieLens przez metadane Crossref (HTTP 200),
- profil https://github.com/Rastythekidd (HTTP 200/206).

Nie udało się potwierdzić pobierania z serwerów Stanford/GroupLens w tym środowisku. Zachowano lokalne archiwa do odtworzenia i kontroli offline.
Nie wyłączano sprawdzania certyfikatów HTTPS.

## Gdzie są szczegóły
- results/kontrola_linkow.csv — czytelna tabela.
- results/kontrola_linkow.json — pełny wynik pierwszego sprawdzenia.
- results/kontrola_linkow_powtorna.json — dodatkowe sprawdzenia.
- sources/source_manifest.json — pochodzenie rekordów i sumy kontrolne.
- data/raw — oryginalne archiwa do pracy lokalnej.

Wyniki opisują dostępność w dniu sprawdzenia, a nie stałą gwarancję działania adresów.

## Repozytorium projektu
Adres przekazany przez użytkownika: https://github.com/Rastythekidd/ml-imdb-movielens
Adres dodano do raportu i konfiguracji. Dostępność zawartości repozytorium nie była w tym kroku sprawdzana; samo dodanie adresu nie oznacza przesłania plików. Nie wykonano zmian na GitHubie.
