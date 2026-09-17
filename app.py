import os
from flask import Flask, render_template, request, redirect
from database import get_db, create_table

app = Flask(__name__)

create_table()


@app.route("/")
def home():
    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM series ORDER BY id DESC")
        rows = cursor.fetchall()

    conn.close()

    # Convert PostgreSQL tuples into dictionaries
    series = [
        {
            "id": row[0],
            "title": row[1],
            "genre": row[2],
            "status": row[3],
            "rating": row[4],
            "episodes": row[5],
            "total_episodes": row[6]
        }
        for row in rows
    ]

    completed = sum(1 for s in series if s["status"] == "Completed")
    ongoing = sum(1 for s in series if s["status"] == "Ongoing")
    yet_to_start = sum(1 for s in series if s["status"] == "Yet to Start")

    return render_template(
        "index.html",
        series=series,
        completed=completed,
        ongoing=ongoing,
        yet_to_start=yet_to_start
    )


@app.route("/add", methods=["POST"])
def add_series():
    title = request.form["title"]
    genre = request.form["genre"]
    status = request.form["status"]
    rating = request.form["rating"] or 0
    episodes = request.form["episodes"] or 0
    total_episodes = request.form["total_episodes"] or 0

    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO series
            (title, genre, status, rating, episodes, total_episodes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            title,
            genre,
            status,
            rating,
            episodes,
            total_episodes
        ))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["POST"])
def edit_series(id):
    title = request.form["title"]
    genre = request.form["genre"]
    status = request.form["status"]
    rating = request.form["rating"] or 0
    episodes = request.form["episodes"] or 0
    total_episodes = request.form["total_episodes"] or 0

    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE series
            SET title = %s,
                genre = %s,
                status = %s,
                rating = %s,
                episodes = %s,
                total_episodes = %s
            WHERE id = %s
        """, (
            title,
            genre,
            status,
            rating,
            episodes,
            total_episodes,
            id
        ))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_series(id):
    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM series WHERE id = %s",
            (id,)
        )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)