from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
pg = psycopg2.connect("""
    host=localhost
    dbname=postgres
    user=postgres
    password=lol1234
    port=5432
""")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country_code = request.form.get('country_code', '').upper()
        return get_country_info(country_code)
    return render_template('index.html')

@app.route('/<country_code>')
def get_country_info(country_code):
    country_code = country_code.upper()  # Приводим код страны к верхнему регистру
    cursor = pg.cursor()
    
    # Запрос для получения названия страны и количества городов
    cursor.execute("""
        SELECT c.name, COUNT(ct.name)
        FROM country c
        LEFT JOIN city ct ON c.code = ct.countrycode
        WHERE c.code = %s
        GROUP BY c.name;
    """, (country_code,))
    
    result = cursor.fetchone()
    
    if not result:
        return "Country not found", 404

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

    return render_template('country_info.html', country_name=country_name, city_count=city_count, cities=cities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
