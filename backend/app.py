"""
Endpoint'ler:
  GET / -> Tum filmleri (year, title) yila göre artan sirali dondurur (Gorev 10)
  GET /movies?year=X -> Belirli yila ait filmleri dondurur (Gorev 11)

"""

from flask import Flask, jsonify, request
from database import get_connection, init_db

app = Flask(__name__)

# Görev 10: Filmleri listele
@app.route("/", methods=["GET"])
def list_movies():
    conn = get_connection()
    # Filmleri yıla göre sırala
    rows = conn.execute(
        "SELECT year, title FROM movies ORDER BY year ASC"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


# Görev 11: Yıla göre filtrele
@app.route("/movies", methods=["GET"])
def get_movies():
    # ?year= değerini al
    year = request.args.get("year")
    conn = get_connection()

    if year is not None:
        # Girilen değerin sayı olup olmadığını kontrol et
        try:
            year_int = int(year)
        except ValueError:
            conn.close()
            # Sayı değilse hata
            return jsonify({"error": "year sayisal bir deger olmalidir."}), 400

        # O yıla ait filmleri getir
        rows = conn.execute(
            "SELECT id, year, title FROM movies WHERE year = ? ORDER BY year ASC",
            (year_int,),
        ).fetchall()
    else:
        # Yıl belirtilmediyse tüm filmleri getir
        rows = conn.execute(
            "SELECT id, year, title FROM movies ORDER BY year ASC"
        ).fetchall()

    conn.close()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)