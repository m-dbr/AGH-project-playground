from flask import Flask, render_template, request, redirect, session
import pyodbc
import hashlib
import config

server = config.DATABASE_SERVER
database = config.DATABASE
username = config.DATABASE_USER
password = config.DATABASE_PASSWORD
driver = config.DATABASE_DRIVER

# Funkcja łącząca do bazy danych
def connect_to_database():
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    cnxn = pyodbc.connect(connection_string)
    return cnxn

def execute_sql_query(query):
    """
    Wykonuje zapytanie SQL na bazie danych i zwraca wynik.
    """
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


# Funkcja pomocnicza do wykonania zapytania do bazy danych i zwracająca wynik w postaci słownika
def execute_query(query):
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Pobranie nazw atrybutów
    column_names = [column[0] for column in cursor.description]

    # Przygotowanie wyniku jako słownik zawierający nazwy atrybutów i ich wartości
    result = []
    for row in rows:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result.append(row_dict)

    # Zamknięcie połączenia z bazą danych
    cursor.close()
    conn.close()

    # Zwrócenie wyniku jako słownik
    return result

# Funkcja szyfrująca hasło
def hash_password(password):
    sha512 = hashlib.sha512()
    sha512.update(password.encode('utf-8'))
    return sha512.digest()



