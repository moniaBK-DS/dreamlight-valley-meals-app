from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("dreamlight_meals.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    search = request.args.get('search', '')
    meal_type = request.args.get('meal_type', '')
    area = request.args.get('area', '')
    star = request.args.get('star', '')

    conn = get_db_connection()

    # Get distinct meal types from the DB
    meal_types = [row['meal'] for row in conn.execute("SELECT DISTINCT meal FROM meals ORDER BY meal").fetchall()]

    # Get distinct areas from the DB
    areas = [row['area'] for row in conn.execute("SELECT DISTINCT area FROM meals ORDER BY area").fetchall()]

    # Get distinct stars class from the DB
    stars = [row['stars'] for row in conn.execute("SELECT DISTINCT stars FROM meals ORDER BY stars").fetchall()]


    # Build query
    query = "SELECT * FROM meals WHERE 1=1"
    params = []

    if search:
        query += " AND (recipe LIKE ? OR ingredients LIKE ?)"
        params.extend((f"%{search}%", f"%{search}%"))

    if meal_type:
        query += " AND meal = ?"
        params.append(meal_type)

    if area:
        query += " AND area = ?"
        params.append(area)

    if star:
        query += " AND stars = ?"
        params.append(star)

    query += " ORDER BY energy DESC"


    meals = conn.execute(query, params).fetchall()
    conn.close()

    return render_template(
        'index.html',
        meals=meals,
        search=search,
        meal_type=meal_type,
        meal_types=meal_types,
        area=area,
        areas=areas,
        star=star,
        stars=stars
    )


if __name__ == '__main__':
    app.run(debug=True)
