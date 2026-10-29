# Wyjaśnienie projektu — etap pierwszy

## 1. Temat i cel
Analizujemy opinie zapisane na dwa sposoby: jako tekst recenzji i jako ocena liczbowa.
Dzięki temu spełniamy wymaganie pracy na danych w języku naturalnym i na danych liczbowych.
W pierwszej części opisujemy dane i formułujemy pytania. Nie trzeba jeszcze przedstawiać wyników modeli.

Krótko na zajęciach:
„Wybraliśmy temat opinii o filmach i innych tytułach IMDb. Porównujemy właściwości tekstowych recenzji i liczbowych ocen. Na razie wykonaliśmy analizę wstępną.”

## 2. Skąd pochodzą dane
IMDb pochodzi z rzeczywistego zbioru Large Movie Review Dataset. Wybrano 200 angielskich recenzji z części train: 100 negatywnych i 100 pozytywnych.
Dobór wykonał skrypt z ustalonym ziarnem 42. Etykiety są oryginalne, nie przewidywał ich model.
11 tekstów zastąpiono rzeczywistymi tekstami tej samej klasy, aby powiązać je z potwierdzonymi nazwami. Zmiany są zapisane w manifeście.

MovieLens pochodzi z MovieLens 100K. Wybrano 200 ocen ze 100 000 rekordów.
Jedna ocena łączy użytkownika, film, wartość 1-5 i czas. Nazwy i rok premiery dodano ze źródłowego u.item.

Plik MovieLens_filmy to czytelny widok MovieLens_liczby. Nie jest trzecim zbiorem.
Nie wolno łączyć recenzji i ocen po ich kolejności w arkuszach.

## 3. Co sprawdzono przed analizą
Sprawdzono braki, powtórzenia, typy danych, zakres ocen oraz zgodność plików.
Każdy tekst i ocenę porównano z oryginalnym archiwum. Nazwy i typy IMDb potwierdzono w zachowanych metadanych.
Nie wykryto błędów wartości. Nie było potrzeby dopisywania lub usuwania rekordów.
W analizie usunięto HTML z kopii tekstu; oryginalne komórki XLSX pozostały bez zmian.

Krótko na zajęciach:
„Dane sprawdziliśmy przed obliczeniami. Braków i duplikatów nie było. Dwa pliki MovieLens opisują dokładnie te same oceny.”

## 4. Co obliczono dla MovieLens
- 200 ocen dotyczy 172 filmów i 161 użytkowników.
- Średnia ocena to 3,42/5; mediana to 3.
- Odchylenie standardowe wynosi około 1,20.
- Najczęstsza ocena: 3, czyli 59 rekordów.
- Oceny 4 i 5 to 98 rekordów, czyli 49%.
- Korelacja Spearmana oceny i roku premiery: około -0,124.

Średnia: suma ocen podzielona przez ich liczbę.
Mediana: środkowa wartość po uporządkowaniu danych.
Odchylenie standardowe: opis rozrzutu ocen.
Spearman: opisuje, czy większym wartościom jednej zmiennej zwykle towarzyszą większe lub mniejsze wartości drugiej; uwzględnia kolejność, a nie tylko odległości liczbowe.

Wynik -0,124 jest bliski zeru i oznacza słaby związek ujemny w tej próbie.
Nie dowodzi wpływu roku na ocenę. Większość filmów ma jedną ocenę, dlatego nie budujemy na tej podstawie rankingu.

## 5. Co obliczono dla IMDb
Po usunięciu HTML policzono tokeny angielskie z liter i opcjonalnego apostrofu.
Nie pomijano stopwords podczas pomiaru długości.

Negatywne recenzje:
- średnia długość: 237,86 słowa;
- mediana: 186 słów.

Pozytywne recenzje:
- średnia długość: 258,92 słowa;
- mediana: 169,5 słowa.

Wyższa średnia i niższa mediana w pozytywnych tekstach nie są sprzecznością. Kilka długich tekstów może podnieść średnią.
Wykres pudełkowy pokazuje duże nakładanie rozkładów. Długość nie rozpoznaje sentymentu w sposób pewny.

Częstość dokumentowa mówi, w ilu recenzjach występuje słowo:
- bad: 43 negatywne i 19 pozytywnych;
- great: 20 negatywnych i 43 pozytywne;
- good: 38 negatywnych i 37 pozytywnych;
- not: 66 negatywnych i 60 pozytywnych.

Słowa występują w różnych kontekstach. Na przykład good może być częścią not good.
Dlatego sama lista słów nie jest jeszcze klasyfikatorem.

## 6. Jak czytać wykresy
- 01_sentiment_balance: pokazuje równowagę 100/100, uzyskaną przez dobór.
- 02_review_length: porównuje rozkłady długości; kreska w pudełku to mediana.
- 03_rating_distribution: liczba ocen od 1 do 5.
- 04_release_decades: ile ocen dotyczy filmów z danej dekady; film może wystąpić kilka razy.
- 05_year_rating: związek roku premiery i oceny; małe przesunięcie punktów służy czytelności.
- 06_negative_words i 07_positive_words: najczęstsze słowa w dokumentach danej klasy.

Wszystkie wykresy są w results/figures. Raport pokazuje wybrane wykresy, aby zachować prostą formę.

## 7. Jakie są ograniczenia
Próby mają po 200 rekordów. Nie reprezentują wszystkich widzów ani wszystkich filmów.
IMDb jest celowo zrównoważony i nie zawiera klasy neutralnej. 11 zamian zależało od dostępności metadanych.
W IMDb są także inne typy tytułów: 167 recenzji dotyczy movie, a 33 pozostałych typów; jest 1 videoGame.
Nie zmieniono próby po zobaczeniu wyników.
MovieLens zawiera historyczne oceny i powtarzających się użytkowników oraz filmy.
Z tych powodów nie wykonano prostego testu istotności traktującego wszystkie rekordy jako niezależne.

## 8. Co robi kod
- src/analysis.py: kontroluje dane wejściowe, oblicza statystyki i tworzy tabele oraz wykresy PDF.
- src/render_figures.py: zapisuje wykresy jako PNG.
- src/make_report.py: składa raport z wyników. Nie oblicza od nowa całej analizy.
- src/run_all.py: uruchamia powyższe kroki.
- src/kontrola_danych.py: porównuje każdy rekord ze źródłem.
- src/reproduce_subset.py: odtwarza dokładnie wybrane dane z oryginalnych archiwów.
- src/tabela_linkow.py: przygotowuje CSV z zapisanej kontroli adresów.
- Analiza_etap_1.ipynb: pozwala przejść przez tę samą analizę w notebooku.

Nie ma osobnego kodu „do wykresów w raporcie” z innymi wynikami. Wszystko korzysta ze wspólnych plików wynikowych.

## 9. Co z linkami
Próba otwarcia linku nie zawsze daje jednoznaczny wynik. IMDb zwraca blokady automatycznego ruchu.
Nie oznacza to, że ID tytułu jest niepoprawny — ID sprawdzono w archiwum i metadanych.
Jeden adres Cinemablend w tekście recenzji jest niedostępny (B91). Pozostawiono go, ponieważ to element autentycznego tekstu.
Szczegóły są w KONTROLA.md i results/kontrola_linkow.csv.

## 10. Co oddajemy i co zostaje na później
Do pierwszego etapu przygotowano raport PDF, dane, źródła, kod, statystyki, wykresy i pytania badawcze.
Repozytorium zostało utworzone przez zespół: https://github.com/Rastythekidd/ml-imdb-movielens. Adres dodano do raportu. Zespół przesyła teraz przygotowane pliki i nadaje dostęp uczestnikom oraz prowadzącemu.
Do Platona wysyła się jeden PDF.

Dalsza część projektu może obejmować:
- porównanie dwóch klasyfikatorów sentymentu;
- dwie metody uczenia bez nadzoru;
- model oparty na transformerach;
- prosty interfejs do przeglądania wyników i predykcji.

Są to plany. W tym raporcie nie ma jeszcze wyników modeli.

## 11. Podział przygotowania do omówienia
- Andrei Rastsiahayeu: temat, źródła, sposób doboru danych i kompletność raportu.
- Vadym Karkhut: MovieLens, statystyki i wykresy ocen.
- Yulia Khrystonko: IMDb, przygotowanie tekstu i długość recenzji.
- Kateryna Ivanchenko: pytania badawcze, wnioski i ograniczenia.
- Alisa Kosenkova: uruchomienie kodu, kontrola wyników i późniejsze przygotowanie repozytorium.

Dodatkowo src/sprawdz_projekt.py sprawdza cały projekt, w tym identyczność wyników po odtworzeniu danych i poprawność adresu repozytorium.
