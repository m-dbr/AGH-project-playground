from flask import Flask, render_template, request, redirect, session, url_for
import re, pyodbc
import fun, config

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = fun.hash_password(password)
    
        query = f"SELECT * FROM uzytkownicy WHERE e_mail = '{email}'"
        tmp = fun.execute_query(query)

        result = {}
        for i in range(len(tmp)):
            result [i]=tmp[i]

        if result:
            stored_password = result[0]['haslo']
            if hashed_password == stored_passw     ord:
                user_data = {
                    'imie': result[0]['imie'],
                    'nazwisko': result[0]['nazwisko'],
                    'e_mail': result[0]['e_mail'],
                }
                return render_template('moje-konto.html', user_data=user_data)  
            else:
                error_msg = "Nieprawidłowe hasło!"
                return render_template('login.html', error=error_msg)
        else:
            error_msg = "Nieprawidłowy e-mail!"
            return render_template('login.html', error=error_msg)
    
    return render_template('login.html')


@app.route('/rejestracja', methods=['GET', 'POST'])
def rejestracja():
    if request.method == 'POST':
        # Pobranie danych z formularza
        email = request.form.get('email')
        password = request.form.get('password')
        imie = request.form.get('imie')
        nazwisko = request.form.get('nazwisko')
        plec = request.form.get('plec')
        telefon = request.form.get('telefon')
        data_urodzenia = request.form.get('data_urodzenia')
        kraj = request.form.get('kraj')
        miasto = request.form.get('miasto')
        ulica = request.form.get('ulica')
        numer_domu = request.form.get('numer_domu')
        kod_pocztowy = request.form.get('kod_pocztowy')

        # Sprawdź, czy użytkownik o podanym emailu już istnieje w bazie danych
        query = f"SELECT COUNT(*) FROM uzytkownicy WHERE e_mail = '{email}'"
        result = fun.execute_query(query)

        if result[0][''] > 0:
            error_msg = 'Użytkownik o podanym e-mailu już istnieje'
            return render_template('rejestracja.html', error=error_msg)

        # Sprawdź, czy hasło spełnia wymagania (od 5 do 15 znaków, przynajmniej jeden znak specjalny i przynajmniej jedna cyfra)
        if len(password) < 5 or len(password) > 15 or not any(c.isdigit() for c in password) or not any(c.isalnum() for c in password):
            error_msg = 'Hasło powinno zawierać od 5 do 15 znaków, jeden znak specjalny i jedną cyfrę'
            return render_template('rejestracja.html', error=error_msg)

        # Wywołaj procedurę składowaną DodajUzytkownika
        query = f"EXEC DodajUzytkownika '{email}', '{password}', '{imie}', '{nazwisko}', '{plec}', '{telefon}', '{data_urodzenia}', '{kraj}', '{miasto}', '{ulica}', '{numer_domu}', '{kod_pocztowy}'"
        fun.execute_sql_query(query)

        msg = 'Rejestracja przebiegła pomyślnie. Możesz teraz się zalogować'
        return render_template('login.html', rejestracja=msg)

    return render_template('rejestracja.html')




if __name__ == '__main__':
    app.run()



# git remote add origin https://github.com/m-dbr/AGH-project-playground.git
# git branch -M main
# git push -u origin main