from flask import Flask, render_template
import psycopg2

app = Flask(__name__)
pg = psycopg2.connect("""
    host=localhost
    dbname=postgres
    user=postgres
    password=lol1234
    port=5432
""")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cities')
def read_count():
    cursor = pg.cursor()
    cursor.execute("SELECT COUNT(*) FROM city WHERE countrycode = 'BRA';")
    pgCount = cursor.fetchone()[0]

    result = str(pgCount) + " (из постгри)"
    return render_template('cities.html', value=result)

@app.route('/<country_code>')
def get_country_info(country_code):
    country_code = country_code.upper()  # Приводим код страны к верхнему регистру

    cursor = pg.cursor()
    
    # Выполняем запрос к базе данных для получения названия страны и количества городов
    cursor.execute("""
        SELECT c.name, COUNT(ct.name)
        FROM country c
        LEFT JOIN city ct ON c.code = ct.countrycode
        WHERE c.code = %s
        GROUP BY c.name;
    """, (country_code,))
    
    result = cursor.fetchone()
    
    if result:
        country_name, city_count = result
        return render_template('country_info.html', country_name=country_name, city_count=city_count)
    else:
        return "Country not found", 404




def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)