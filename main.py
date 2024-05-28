from flask import Flask, render_template, request, session
from flask_session import Session 
import random
import psycopg2

app = Flask(__name__)
pg = psycopg2.connect("""
    host=localhost
    dbname=postgres
    user=postgres
    password=lol1234
    port=5432
""")


# Настройки для сессии
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Список фраз для отображения
phrases = [
    "Когда я ем — я глух и нем. Когда я пью — я гораздо коммуникабельней!",
    "Смерть — это защитная реакция организма на нездоровый образ жизни.",
    "Как тут попадёшь в рай, если пять из семи смертных грехов — это мои хобби?",
    "Сила нужна, чтобы наносить удары. Выносливость — чтобы держать удары. Ловкость — чтобы избегать ударов. А интеллект... Ну, вообще-то за него и бьют.",
    "Ученье — свет, а неученье опасно для здоровья."
]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country_code = request.form.get('country_code', '').upper()
        return get_country_info(country_code)
    return render_template('index.html')

@app.route('/<country_code>')
def get_country_info(country_code):
    country_code = country_code.upper()  # Приводим код страны к верхнему регистру
    session['requests'] = session.get('requests', 0) + 1  # Увеличиваем счетчик запросов
    print("Requests count:", session['requests'])  

    cursor = pg.cursor()
    
    # Запрос для получения названия страны и количества городов
    cursor.execute("""
        SELECT c.name, COUNT(ct.name)
        FROM country c
        LEFT JOIN city ct ON c.code = ct.countrycode
        WHERE c.code = %s
        GROUP BY c.name;
    """, (country_code,))
    
    # Добавляем случайную фразу, если нужно
    random_phrase = None
    if session['requests'] % 3 == 0:
        random_phrase = random.choice(phrases)

    result = cursor.fetchone()
    
    if not result:
        return render_template('country_not_found.html', random_phrase=random_phrase), 404

    country_name, city_count = result

    # Запрос для получения топ-10 крупнейших городов
    cursor.execute("""
        SELECT name, population
        FROM city
        WHERE countrycode = %s
        ORDER BY population DESC
        LIMIT 10;
    """, (country_code,))

    cities = cursor.fetchall()

    return render_template('country_info.html', country_name=country_name, city_count=city_count, cities=cities, random_phrase=random_phrase)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
