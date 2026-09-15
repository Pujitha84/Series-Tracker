import os
from flask import Flask, render_template, request, redirect
from database import get_db, create_table

app = Flask(__name__)

create_table()


@app.route("/")
def home():
    conn = get_db()
    series = conn.execute("SELECT * FROM series ORDER BY id DESC").fetchall()
    conn.close()

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

    conn.execute("""
        INSERT INTO series
        (title, genre, status, rating, episodes, total_episodes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, genre, status, rating, episodes, total_episodes))

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

    conn.execute("""
        UPDATE series
        SET title = ?,
            genre = ?,
            status = ?,
            rating = ?,
            episodes = ?,
            total_episodes = ?
        WHERE id = ?
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
    conn.execute("DELETE FROM series WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)