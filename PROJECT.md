# System do zarządzania flotą samochodową w firmie

## Skład:
* Adrian Kacorzyk
* Rafał Szczepańczyk
* Arkadiusz Juszczyk


## Modele w systemie:
* Firma (dane firmy)
* Użytkownik
  * pracownik
  * administrator
* Pojazd



## Funkcjonalności:

* Użytkownicy:
  * Logowanie jako pracownik
  * Logowanie jako administrator
  * Wylogowanie użytkownika
  * Zmiana hasła użytkownika
  * [Admin] Tworzenie użytkownika
  * Zmiana użytkownika
* Pojazdy:
  * Tworzenie pojazdu
  * Edycja pojazdu
  * Usunięcie pojazdu
  * Rezerwacja/przypisanie pojazdu dla pracownika
  * 
  
## Przypadki testowe
Użytkownicy
<details>
  <summary>Logowanie jako pracownik - Niepoprawne dane</summary>
  <ul>
    <li>Otwórz stronę logowania aplikacji.</li>
    <li>Wprowadź niepoprawną nazwę użytkownika lub hasło pracownika.</li>
    <li>Kliknij przycisk "Zaloguj się".</li>
    <li>Oczekiwany wynik: Pojawia się komunikat błędu informujący o niepoprawnych danych logowania.</li>
  </ul>
</details>
<details>
  <summary>Logowanie jako administrator - Poprawne dane</summary>
  <ul>
    <li>Otwórz stronę logowania aplikacji.</li>
    <li>Wprowadź poprawną nazwę użytkownika i hasło administratora.</li>
    <li>Kliknij przycisk "Zaloguj się".</li>
    <li>Oczekiwany wynik: Użytkownik zostaje przekierowany do strony głównej aplikacji dla administratorów.</li>
  </ul>
</details>
<details>
  <summary>Wylogowanie użytkownika</summary>
  <ul>
    <li>Zaloguj się do aplikacji jako użytkownik (pracownik lub administrator).</li>
    <li>Kliknij przycisk "Wyloguj się".</li>
    <li>Oczekiwany wynik: Użytkownik zostaje wylogowany i przekierowany na stronę logowania.</li>
  </ul>
</details>
<details>
  <summary>Zmiana hasła użytkownika - Niepoprawne obecne hasło</summary>
  <ul>
    <li>Zaloguj się jako użytkownik.</li>
    <li>Przejdź do sekcji zmiany hasła.</li>
    <li>Wprowadź niepoprawne obecne hasło, a następnie nowe hasło zgodnie z wymogami bezpieczeństwa.</li>
    <li>Kliknij przycisk "Zmień hasło".</li>
    <li>Oczekiwany wynik: Pojawia się komunikat błędu informujący o niepoprawnym obecnym haśle.</li>
  </ul>
</details>
<details>
  <summary>[Admin] Tworzenie użytkownika - Niekompletne dane</summary>
  <ul>
    <li>Zaloguj się jako administrator.</li>
    <li>Przejdź do sekcji tworzenia nowego użytkownika.</li>
    <li>Wprowadź tylko część wymaganych danych (np. pomijając adres e-mail).</li>
    <li>Kliknij przycisk "Utwórz użytkownika".</li>
    <li>Oczekiwany wynik: Pojawia się komunikat błędu informujący o brakujących danych.</li>
  </ul>
</details>
<details>
  <summary>Zmiana użytkownika - Duplikat danych</summary>
  <ul>
    <li>Zaloguj się jako administrator.</li>
    <li>Przejdź do sekcji edycji użytkownika.</li>
    <li>Zmień adres e-mail na taki, który już istnieje w systemie.</li>
    <li>Kliknij przycisk "Zapisz zmiany".</li>
    <li>Oczekiwany wynik: Pojawia się komunikat błędu informujący o duplikacie adresu e-mail.</li>
  </ul>
</details>
Pojazdy
<details>
  <summary>Edycja pojazdu - Niekompletne dane</summary>
  <ul>
    <li>Zaloguj się jako administrator.</li>
    <li>Przejdź do sekcji edycji pojazdu.</li>
    <li>Usuń jedno z wymaganych pól, np. numer rejestracyjny.</li>
    <li>Kliknij przycisk "Zapisz zmiany".</li>
    <li>Oczekiwany wynik: Pojawia się komunikat błędu informujący o niekompletnych danych.</li>
  </ul>
</details>
<details>
  <summary>Usunięcie pojazdu - Nieistniejący pojazd</summary>
  <ul>
    <li>Zaloguj się jako administrator.</li>
    <li>Próbuj usunąć pojazd, który został już usunięty lub nie istnieje w bazie danych.</li>
    <li>Oczekiwany wynik: Pojawia się komunikat błędu informujący, że pojazd nie istnieje.</li>
  </ul>
</details>
<details>
  <summary>Rezerwacja pojazdu dla pracownika - Przypisanie pojazdu, który już jest przypisany</summary>
  <ul>
    <li>Zaloguj się jako administrator.</li>
    <li>Przejdź do sekcji zarządzania pojazdami.</li>
    <li>Wybierz pojazd, który jest już przypisany do innego pracownika.</li>
    <li>Próbuj przypisać ten pojazd innemu pracownikowi.</li>
    <li>Oczekiwany wynik: Pojawia się komunikat błędu informujący, że pojazd jest już przypisany.</li>
  </ul>
</details>
