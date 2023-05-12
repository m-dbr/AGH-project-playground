import pyodbc
import config

# Konfiguracja połączenia z bazą danych SQL Server
server = config.DATABASE_SERVER
database = config.DATABASE
username = config.DATABASE_USER
password = config.DATABASE_PASSWORD
driver = config.DATABASE_DRIVER


# Tworzenie łańcucha połączenia
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(connection_string)
    print('Połączenie z bazą danych jest aktywne!')

    # Tworzenie obiektu kursora
    cursor = conn.cursor()

    # Przykładowe zapytanie SELECT
    query = "SELECT * FROM uzytkownicy"

    # Wykonanie zapytania
    cursor.execute(query)

    # Pobranie wyników zapytania
    results = cursor.fetchall()

    # Wyświetlenie wyników na ekranie
    for row in results:
        print(row)

    # Zamknięcie kursora i połączenia
    cursor.close()
    conn.close()

except pyodbc.Error as ex:
    print('Błąd połączenia z bazą danych:', ex)