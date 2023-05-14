from flask import Flask, render_template, request, redirect, session
import pyodbc
import hashlib
import config

server = config.DATABASE_SERVER
database = config.DATABASE
username = config.DATABASE_USER
password = config.DATABASE_PASSWORD
driver = config.DATABASE_DRIVER


def connect_to_database():
    """
    Połącznie z bazą danych
    """
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    cnxn = pyodbc.connect(connection_string)
    return cnxn


def execute_sql_query(query, params=None):
    """
    Wykonuje zapytanie SQL na bazie danych i zwraca wynik.
    """
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()


def execute_query(query, params=None):
    """
    Funkcja wykonująca zapytanie SQL i zwracająca słownik
    """
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
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

def hash_password(password):
    """
    Funkcja szyfrująca hasło
    """
    sha512 = hashlib.sha512()
    sha512.update(password.encode('utf-8'))
    return sha512.digest()

def user_data(email=None, id_user=None):
    if email is not None:
        tmp = execute_query('SELECT * FROM uzytkownicy WHERE e_mail=?', (email,))
    elif id_user is not None:
        tmp = execute_query('SELECT * FROM uzytkownicy WHERE id_uzytkownika=?', (id_user,))

    result = {}
    for i in range(len(tmp)):
        result [i]=tmp[i]
    
    if result:
        user_data = {
            'id_user': result[0]['id_uzytkownika'],
            'imie': result[0]['imie'],
            'nazwisko': result[0]['nazwisko'],
            'e_mail': result[0]['e_mail'],
            'haslo': result[0]['haslo'],
            'plec': result[0]['plec'],
            'telefon': result[0]['telefon'],
            'data_urodzenia': result[0]['data_urodzenia'],
            'kraj': result[0]['kraj'],
            'miasto': result[0]['miasto'],
            'ulica': result[0]['ulica'],
            'numer_domu': result[0]['numer_domu'],
            'kod_pocztowy': result[0]['kod_pocztowy']
        }
        return user_data
    return False


