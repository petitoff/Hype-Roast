# Hype Roast

Jest to projekt, który zawiera programu do analizy cen kryptowaluty w platofmie Coinbase.

### Użyty język programowania:
* Python 3.9

### Użyte biblioteki:
* coinbase
* python-telegram-bot

## Opis i funkcje
[Dodatkowe informacje](https://petitoff.gitbook.io/hype-roast/)

Program pobiera informacje o cenach z api coinbase a następnie zapisuje je do wewnętrznego słownika do dalszej analizy. Program opiera swoje działanie na apliacki zewnętrznej [Telegram](https://telegram.org/). Steruje się dzięki niej ustawieniami programu. Dodaje ceny alarmowe oraz dostaje powiadomienia o skokach cen. 

## Użytkowanie
Program może być dostępny jako gotowy produkt ale do własnego skonfigurowania z uwagi na własne api coinbase oraz telegram. Api w programie nie zostało zaimplementowane z uwagi na bezpieczeństwo. Powinno być umieszczone w zewnętrznym pliku. W programie w wersji dev oraz na gotowej produkcji jest umieszczone w osobnym pliku json.
