**kcalkulator** to aplikacja służąca do zarządzania profilami użytkowników oraz monitorowania masy ciała, wartości BMI i zapotrzebowania kalorycznego. Jej celem jest wsparcie użytkownika w efektywnym zarządzaniu dietą i aktywnością fizyczną poprzez dostarczanie kluczowych danych, takich jak:
- Obliczanie wartości BMI i kategoryzacja na podstawie wagi i wzrostu.
- Monitorowanie historii wag, BMI i zapotrzebowania kalorycznego.
- Obliczanie "zera kalorycznego" (TDEE) z uwzględnieniem poziomu aktywności i wieku.
- Wyliczenia zapotrzebowania kalorii dla przybierania bądź redukcji masy ciała.
- Obsługa profili użytkowników i historii pomiarów.


**Wymagania wstępne**
Aby uruchomić projekt **kcalkulator**, należy upewnić się, że spełnione są poniższe wymagania:
- Python w wersji 3.10 lub wyższej.
- Zainstalowane biblioteki:
    - `numpy`
    - `scikit-learn`
    - `sqlite3` (wbudowana w Python)
    - `PyQt6`
    - `matplotlib`



**Struktura projektu**
Projekt składa się z kilku modułów odpowiedzialnych za różne funkcjonalności:
**Moduły**
- **`main_classes.py`:** Zawiera klasy do obliczeń związanych z BMI oraz zapotrzebowaniem kalorycznym:
    - `BmiCalculator` - Oblicza wartość BMI i określa kategorię wagową.
    - `CaloricDemandCalculator` - Wyznacza "zero kaloryczne" (ang. TDEE) na podstawie masy ciała, wieku, wzrostu i poziomu aktywności.
    - `CaloricDemandAdjuster` - Kalkuluje nadwyżkę i deficyt kaloryczny do celów diety.

- **`database.py`:** Odpowiada za zarządzanie bazą danych SQLite:
    - Tworzenie, zapisywanie i usuwanie profili użytkowników.
    - Historia pomiarów wag, BMI i zapotrzebowania kalorycznego.
    - Import/eksport danych profili z/do plików.

- **`main_gui.py`:** Obsługuje interfejs użytkownika stworzony przy użyciu PyQt6. Zawiera funkcje odpowiedzialne za nawigację między widokami, obsługę danych użytkownika i generowanie wykresów.


**Obsługa aplikacji**
Importowanie profilu: Na początku należy przejść do zakładki „Zarządzanie profilami” i zaimportować profil lub profile. Jeśli dojdzie do pomyłki, jest możliwość usunięcia błędnie dodanego profilu.

Wybór profilu: Po zaimportowaniu profilu, przechodzimy do menu głównego i wybieramy interesujący nas profil, aby przejść do kolejnych funkcji.

Podsumowanie profilu: Po wybraniu profilu, aplikacja wyświetli szczegółowe podsumowanie wszystkich informacji dotyczących tego profilu.

Eksportowanie podsumowania: W prawym górnym rogu ekranu znajduje się opcja wyeksportowania podsumowania. Dzięki temu możesz zapisać lub udostępnić dane profilu.

Aktualizowanie danych: Istnieje możliwość aktualizacji profilu o nową wagę oraz datę jej zmierzenia. W tym celu wystarczy kliknąć przycisk "+" obok etykiety wagi.
