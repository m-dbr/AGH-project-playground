from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta, date

import fun

app = Flask(__name__)

app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
    """
    Strona główna aplikcji
    """
    if 'id_user' in session:
        msg = f"Zalogowany jako: {session['id_user']}"
        user_data = fun.user_data(email=None, id_user=session['id_user'])
        return render_template('index.html', msg=msg, user_data=user_data)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Strona logowania
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # wywłouje funkcję hashującą wprowadzone hasło,
        # które jest porównywane z hasłem z bazy danych
        hashed_password = fun.hash_password(password)
    
        # pobiera dane użytkownika o zadanym email lub id_user
        user_data = fun.user_data(email=email, id_user=None)

        if user_data:
            stored_password = user_data['haslo']
            if hashed_password == stored_password:
                session['id_user'] = user_data['id_user']
                session.permanent = True
                app.permanent_session_lifetime = timedelta(hours=2)

                # jeżeli dane są poprawne następuje wpisanie id_uzytkownika do sesji
                # przekierowanie do strony moje-konto
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
    """
    Funkcjonalność usuwająca id_uzytkownika z sesji
    """
    session.pop('id_user', None)
    return redirect(url_for('index'))


@app.route('/rejestracja', methods=['GET', 'POST'])
def rejestracja():
    """
    Rejestracja nowego użytkownika
    """
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

        # Sprawdzenie, czy użytkownik o podanym emailu już istnieje w bazie danych
        result = fun.execute_query('SELECT COUNT(*) FROM uzytkownicy WHERE e_mail=?', (email,))

        if result[0][''] > 0:
            error_msg = 'Użytkownik o podanym e-mailu już istnieje'
            return render_template('rejestracja.html', error=error_msg)

        # Sprawdzenie, czy hasło spełnia wymagania (od 5 do 15 znaków, przynajmniej jeden znak specjalny i przynajmniej jedna cyfra)
        if len(password) < 5 or len(password) > 15 or not any(c.isdigit() for c in password) or not any(c.isalnum() for c in password):
            error_msg = 'Hasło powinno zawierać od 5 do 15 znaków, jeden znak specjalny i jedną cyfrę'
            return render_template('rejestracja.html', error=error_msg)

        # Wywołanie procedurę składowaną DodajUzytkownika
        query = "EXEC DodajUzytkownika ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
        params = (email, password, imie, nazwisko, plec, telefon, data_urodzenia, kraj, miasto, ulica, numer_domu, kod_pocztowy)

        fun.execute_sql_query(query, params)

        msg = 'Rejestracja przebiegła pomyślnie. Możesz teraz się zalogować'
        return render_template('login.html', rejestracja=msg)

    return render_template('rejestracja.html')

@app.route('/moje-konto')
def dashboard():
    """
    Strona dostępna po zalogowaniu
    """
    # pobieranie danych użytkownika
    user_data = fun.user_data(email=None, id_user=session['id_user'])
    if user_data:
        return render_template('moje-konto.html', user_data=user_data)

@app.route('/moje-dane')
def user_data():
    """
    Strona zawierająca szczegółowe informacje o danym użytkowniku
    """
    # pobieranie danych użytkownika
    user_data = fun.user_data(email=None, id_user=session['id_user'])
    if user_data:
        return render_template('moje-dane.html', user_data=user_data)

@app.route('/edytuj-dane', methods=['GET', 'POST'])
def edytuj_dane():
    """
    Strona pozwalająca na edycję danych
    """
    if request.method == 'POST':
        # pobieranie danych użytkownika
        user_data = fun.user_data(email=None, id_user=session['id_user'])

        # pobieranie danych z formularza
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

        # sprawdzenie, czy hasło spełnia wymagania (od 5 do 15 znaków, przynajmniej jeden znak specjalny i przynajmniej jedna cyfra)
        if password != '':
            if len(password) < 5 or len(password) > 15 or not any(c.isdigit() for c in password) or not any(c.isalnum() for c in password):
                msg = 'Hasło powinno zawierać od 5 do 15 znaków, jeden znak specjalny i jedną cyfrę'
                return render_template('edytuj-dane.html', msg=msg)

        # wywołanie procedury składowanej DodajUzytkownika
        query = "EXEC EdytujUzytkownika ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
        params = (session['id_user'], password, imie, nazwisko, plec, telefon, data_urodzenia, kraj, miasto, ulica, numer_domu, kod_pocztowy)

        fun.execute_sql_query(query, params)

        # pobranie danych użytkownika
        user_data = fun.user_data(email=None, id_user=session['id_user'])
        if user_data:
            msg = 'Zmiana danych przebiegła pomyślnie'
            return render_template('moje-dane.html', msg=msg, user_data=user_data)
    
    user_data = fun.user_data(email=None, id_user=session['id_user'])
    return render_template('edytuj-dane.html', user_data=user_data)


@app.route('/kursy')
def courses():
    """
    Strona z kursami dostępna dla zalogowanych i niezalogowanych użytkowników
    """
    # Pobranie listy kursów z bazy danych
    cursor = fun.connect_to_database().cursor()
    cursor.execute('SELECT * FROM Vkursy_poziomy_widok')
    kursy = cursor.fetchall()
    cursor.close()
    fun.connect_to_database().close()

    if 'id_user' in session:
        user_data = fun.user_data(email=None, id_user=session['id_user']) 
        return render_template('kursy.html', kursy=kursy, user_data=user_data)
    return render_template('kursy.html', kursy=kursy)


@app.route('/kup-kurs/<int:id_kursu>')
def buy_course(id_kursu):
    """
    Funkcjonalność kupienie kursu. Jeżeli niezalogowany: kupuje kurs. Jeżeli niezalogowany: przekierowanie do strony logowania
    """
    if 'id_user' in session:
        # pobranie danych - sprawdzenie czy uzytkownik juz ma kupiony dany kurs
        result0 = fun.execute_query('SELECT * FROM zamowienia_kursy WHERE id_kursu=? AND id_uzytkownika=?', (id_kursu, session['id_user']))

        # jeżeli kurs widnieje w tabeli zamowienia_kursy
        if result0:
            flash('Sprawdź swoje kursy! Już masz ten kurs')
            return redirect(url_for('courses'))

        # pobieranie danych kursu
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
            }
        current_date = date.today().strftime('%Y-%m-%d')
        # Aktualizacja danych zamówienia
        # Dodanie oplacenia jako dzien dzisiejszy - brak implementacji platnosci jeszcze
        fun.execute_sql_query('INSERT INTO zamowienia_kursy (id_kursu, id_uzytkownika, data_zlozenia, data_oplacenia, typ_platnosci) VALUES (?, ?, ?, ?, ?)', (kursy['id_kursu'], session['id_user'], current_date, current_date, 'Blik'))
        
        flash('Kurs zakupiono!')

        return redirect(url_for('courses'))
    else:
        return redirect(url_for('login'))


@app.route('/moje-kursy')
def my_courses():
    """
    Strona wyświetlająca zakupione kursy
    """
    # Pobranie zakupionych kursów z bazy danych
    cursor = fun.connect_to_database().cursor()
    cursor.execute(f"SELECT * FROM Vszczegoly_zamowien_kursy where id_uzytkownika={session['id_user']}")
    moje_kursy = cursor.fetchall()
    cursor.close()
    fun.connect_to_database().close()

    if 'id_user' in session:
        user_data = fun.user_data(email=None, id_user=session['id_user']) 

        # Pobieranie ulubionych kursów użytkownika
        cursor = fun.connect_to_database().cursor()
        cursor.execute(f"SELECT * FROM ulubione_kursy WHERE id_uzytkownika={session['id_user']}")
        ulubione_kursy = cursor.fetchall()
        cursor.close()
        fun.connect_to_database().close()

        ulubione_kursy_ids = [tup[0] for tup in ulubione_kursy]
        return render_template('moje-kursy.html', moje_kursy=moje_kursy, user_data=user_data, ulubione_kursy_ids=ulubione_kursy_ids)
    
    return render_template('kursy.html', moje_kursy=moje_kursy)

@app.route('/dodaj-do-ulubionych', methods=['POST'])
def add_to_favorites():
    """
    Funkcjonalność dodania danego kursu do ulubionych
    """
    if 'id_user' in session:
        id_zamowienia_kursy = request.form.get('id_zamowienia_kursy')
        id_user = session['id_user']
        # Sprawdzenie, czy kurs już istnieje w tabeli ulubione_kursy
        cursor = fun.connect_to_database().cursor()

        cursor.execute(f"SELECT * FROM ulubione_kursy WHERE id_uzytkownika={id_user} AND id_zamowienia_kursy={id_zamowienia_kursy}")
        existing_favorite = cursor.fetchone()
        cursor.close()
        fun.connect_to_database().close()
    
        if existing_favorite:
            flash("Kurs jest już w ulubionych.")
        else:
            # Dodanie kursu do ulubionych
            fun.execute_sql_query("INSERT INTO ulubione_kursy (id_zamowienia_kursy, id_uzytkownika) VALUES (?, ?)", (id_zamowienia_kursy, id_user))

            return redirect(url_for('my_courses'))

    return redirect('/moje-kursy')


@app.route('/odtworz/<int:id_zamowienia_kursy>')
def play(id_zamowienia_kursy):
    """
    Odtworzenie kursu z adresu URL
    """
    # Pobierz URL z bazy danych na podstawie kurs_id
    cursor = fun.connect_to_database().cursor()
    cursor.execute('SELECT adres_url FROM Vszczegoly_zamowien_kursy WHERE id_zamowienia_kursy = ?', (id_zamowienia_kursy,))
    adres_url = cursor.fetchone()[0]
    print(adres_url)
    return render_template('odtworz-kurs.html', adres_url=adres_url)


@app.route('/ulubione-kursy')
def favorite_courses():
    """
    Strona zawierająca listę ulubionych kursów
    """
    if 'id_user' in session:
        id_user = session['id_user']

        # Pobranie ulubionych kursów użytkownika z bazy danych
        cursor = fun.connect_to_database().cursor()
        cursor.execute(f"SELECT * FROM Vulubione_kursy WHERE id_uzytkownika={id_user}")
        ulubione_kursy = cursor.fetchall()
        cursor.close()
        fun.connect_to_database().close()

        print(ulubione_kursy)

        return render_template('ulubione-kursy.html', ulubione_kursy=ulubione_kursy)
    
    return redirect('/login')  # Przekierowanie do strony logowania, jeśli użytkownik nie jest zalogowany


@app.route('/usun-ulubiony-kurs', methods=['POST'])
def remove_favorite_course():
    """
    Funkcjonalność usuwająca ulubiony kurs z bazy danych
    """
    if 'id_user' in session:
        id_zamowienia_kursy = request.form.get('id_zamowienia_kursy')
        redirect_page = request.form.get('redirect_page')
        id_user = session['id_user']

        # Aktualizacja rekordu w tabeli ulubione_kursy
        fun.execute_sql_query("DELETE FROM ulubione_kursy WHERE id_uzytkownika=? AND id_zamowienia_kursy=?", (id_user, id_zamowienia_kursy))

        flash("Kurs został usunięty z ulubionych.")
    if redirect_page == 'ulubione-kursy':
        return redirect('/ulubione-kursy')
    elif redirect_page == 'moje-kursy':
        return redirect('/moje-kursy')


if __name__ == '__main__':
    app.run()

