from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta, date
import re, pyodbc
import fun, config

app = Flask(__name__)

app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
    if 'id_user' in session:
        msg = f"Zalogowany jako: {session['id_user']}"
        user_data = fun.user_data(email=None, id_user=session['id_user'])
        return render_template('index.html', msg=msg, user_data=user_data)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = fun.hash_password(password)
        
        user_data = fun.user_data(email=email, id_user=None)

        if user_data:
            stored_password = user_data['haslo']
            if hashed_password == stored_password:
                session['id_user'] = user_data['id_user']
                session.permanent = True
                app.permanent_session_lifetime = timedelta(hours=2)
                return redirect(url_for('dashboard', user_data=user_data))
            else:
                error_msg = "Nieprawidłowe hasło!"
                return render_template('login.html', error=error_msg)
        else:
            error_msg = "Nieprawidłowy e-mail!"
            return render_template('login.html', error=error_msg)
    
    return render_template('login.html')

@app.route('/wyloguj')
def logout():
    session.pop('id_user', None)
    return redirect(url_for('index'))


@app.route('/rejestracja', methods=['GET', 'POST'])
def rejestracja():
    if request.method == 'POST':
        # Pobranie danych z formularza
        email = request.form.get('email')
        password = request.form.get('password')
        imie = request.form.get('imie')
        nazwisko = request.form.get('nazwisko')
        plec = request.form.get('plec')
        if plec == '' or plec == 'Wybierz':
            plec = None
        telefon = request.form.get("telefon")
        if telefon == '':
            telefon = None
        data_urodzenia = request.form.get('data_urodzenia')
        if data_urodzenia == '':
            data_urodzenia = None
        kraj = request.form.get('kraj')
        if kraj == '':
            kraj = None
        miasto = request.form.get('miasto')
        if miasto == '':
            miasto = None
        ulica = request.form.get('ulica')
        if ulica == '':
            ulica = None
        numer_domu = request.form.get('numer_domu')
        if numer_domu == '':
            numer_domu = None
        kod_pocztowy = request.form.get('kod_pocztowy')
        if kod_pocztowy == '':
            kod_pocztowy = None

        # Sprawdź, czy użytkownik o podanym emailu już istnieje w bazie danych
        result = fun.execute_query('SELECT COUNT(*) FROM uzytkownicy WHERE e_mail=?', (email,))

        if result[0][''] > 0:
            error_msg = 'Użytkownik o podanym e-mailu już istnieje'
            return render_template('rejestracja.html', error=error_msg)

        # Sprawdź, czy hasło spełnia wymagania (od 5 do 15 znaków, przynajmniej jeden znak specjalny i przynajmniej jedna cyfra)
        if len(password) < 5 or len(password) > 15 or not any(c.isdigit() for c in password) or not any(c.isalnum() for c in password):
            error_msg = 'Hasło powinno zawierać od 5 do 15 znaków, jeden znak specjalny i jedną cyfrę'
            return render_template('rejestracja.html', error=error_msg)

        # Wywołaj procedurę składowaną DodajUzytkownika
        query = "EXEC DodajUzytkownika ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
        params = (email, password, imie, nazwisko, plec, telefon, data_urodzenia, kraj, miasto, ulica, numer_domu, kod_pocztowy)

        fun.execute_sql_query(query, params)

        msg = 'Rejestracja przebiegła pomyślnie. Możesz teraz się zalogować'
        return render_template('login.html', rejestracja=msg)

    return render_template('rejestracja.html')

@app.route('/moje-konto')
def dashboard():
    user_data = fun.user_data(email=None, id_user=session['id_user'])
    if user_data:
        return render_template('moje-konto.html', user_data=user_data)

@app.route('/moje-dane')
def user_data():
    user_data = fun.user_data(email=None, id_user=session['id_user'])
    if user_data:
        return render_template('moje-dane.html', user_data=user_data)

@app.route('/edytuj-dane', methods=['GET', 'POST'])
def edytuj_dane():
    if request.method == 'POST':
        user_data = fun.user_data(email=None, id_user=session['id_user'])

        # Pobierz dane z formularza
        password = request.form.get('password')
        imie = request.form.get('imie')
        if imie == '':
            imie = None
        nazwisko = request.form.get('nazwisko')
        if nazwisko == '':
            nazwisko = None
        plec = request.form.get('plec')
        if plec == '' or plec == 'Wybierz':
            plec = None
        telefon = request.form.get("telefon")
        if telefon == '':
            telefon = None
        data_urodzenia = request.form.get('data_urodzenia')
        if data_urodzenia == '':
            data_urodzenia = None
        kraj = request.form.get('kraj')
        if kraj == '':
            kraj = None
        miasto = request.form.get('miasto')
        if miasto == '':
            miasto = None
        ulica = request.form.get('ulica')
        if ulica == '':
            ulica = None
        numer_domu = request.form.get('numer_domu')
        if numer_domu == '':
            numer_domu = None
        kod_pocztowy = request.form.get('kod_pocztowy')
        if kod_pocztowy == '':
            kod_pocztowy = None


        # Sprawdź, czy hasło spełnia wymagania (od 5 do 15 znaków, przynajmniej jeden znak specjalny i przynajmniej jedna cyfra)
        if password != '':
            if len(password) < 5 or len(password) > 15 or not any(c.isdigit() for c in password) or not any(c.isalnum() for c in password):
                msg = 'Hasło powinno zawierać od 5 do 15 znaków, jeden znak specjalny i jedną cyfrę'
                return render_template('edytuj-dane.html', msg=msg)

        # Wywołaj procedurę składowaną DodajUzytkownika
        query = "EXEC EdytujUzytkownika ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
        params = (session['id_user'], password, imie, nazwisko, plec, telefon, data_urodzenia, kraj, miasto, ulica, numer_domu, kod_pocztowy)

        fun.execute_sql_query(query, params)

        user_data = fun.user_data(email=None, id_user=session['id_user'])
        if user_data:
            msg = 'Zmiana danych przebiegła pomyślnie'
            return render_template('moje-dane.html', msg=msg, user_data=user_data)
    
    user_data = fun.user_data(email=None, id_user=session['id_user'])
    return render_template('edytuj-dane.html', user_data=user_data)


@app.route('/kursy')
def courses():
    # Pobranie listy kursów z bazy danych
    view = 'Vszczegoly_kursy'
    tmp = fun.execute_query('SELECT * FROM Vszczegoly_kursy')

    result = {}
    for i in range(len(tmp)):
        result [i]=tmp[i]
    
    if result:
        kursy = {
            'id_kursu': result[0]['id_kursu'],
            'nazwa': result[0]['nazwa'],
            'autor': result[0]['autor'],
            'cena': result[0]['cena'],
            'data_dodania': result[0]['data_dodania'],
            'czas_trwania': result[0]['czas_trwania'],
            'adres_url': result[0]['adres_url'],
            'nazwa_poziomu': result[0]['nazwa_poziomu']
        }
    print('!!!!!!!!!!!!!!!')
    print(kursy)
    
    if 'id_user' in session:
        user_data = fun.user_data(email=None, id_user=session['id_user']) 
        return render_template('kursy.html', kursy=kursy, user_data=user_data)
    return render_template('kursy.html', kursy=kursy)

# Kupowanie kursu
@app.route('/kup-kurs/<int:id_kursu>')
def buy_course(id_kursu):
    if 'id_user' in session:
        # Pobranie danych kursu
        tmp = fun.execute_query('SELECT * FROM kursy WHERE id_kursu=?', (id_kursu,))

        result = {}
        for i in range(len(tmp)):
            result [i]=tmp[i]
        
        if result:
            kursy = {
                'id_kursu': result[0]['id_kursu'],
                'nazwa': result[0]['nazwa'],
                'autor': result[0]['autor'],
                'cena': result[0]['cena'],
                'data_dodania': result[0]['data_dodania'],
                'czas_trwania': result[0]['czas_trwania'],
                'adres_url': result[0]['adres_url'],
                'nazwa_poziomu': result[0]['nazwa_poziomu']
            }
        current_date = date.today().strftime('%Y-%m-%d')
        # Aktualizacja danych zamówienia
        fun.execute_sql_query('INSERT INTO zamowienia_kursy (id_kursu, id_uzytkownika, data_zlozenia, data_oplacenia, typ_platnosci) VALUES (?, ?, ?, ?, ?, ?)', (kursy['id_kursu'], session['id_user'], current_date, current_date, 'Blik'))
        
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()

