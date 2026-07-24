"""
Endpoint'ler:
  GET / -> Tum filmleri (year, title) yila göre artan sirali dondurur (Gorev 10)
  GET /movies?year=X -> Belirli yila ait filmleri dondurur (Gorev 11)
  POST /movies -> Yeni film ekler, body: year, title (Gorev 12)
  DELETE /movies?year=X -> Query param ile o yildaki filmleri siler (Gorev 13)
  DELETE /movies/<year> -> Path param ile o yildaki filmleri siler (Gorev 14)
  GET /search?title=X -> title alaninda LIKE ile arama yapar (Gorev 15)
  PUT /movies -> Mevcut filmi gunceller, body: id, year, title (Gorev 21)
  
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection, init_db

app = Flask(__name__)
CORS(app)

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

# Görev 12: Film ekle
@app.route("/movies", methods=["POST"])
def add_movie():
    # Veri paketini al
    data = request.get_json(silent=True)
    
    # Veri gönderilmemişse uyar
    if not data:
        return jsonify({"error": "JSON govdesi bekleniyor."}), 400

    year = data.get("year")
    title = data.get("title")

    # Yıl veya başlık eksikse uyar
    if year is None or not title:
        return jsonify({"error": "'year' ve 'title' alanlari zorunludur."}), 400

    # Yıl sayı formatında değilse uyar 
    try:
        year_int = int(year)
    except (ValueError, TypeError):
        return jsonify({"error": "'year' sayisal bir deger olmalidir."}), 400

    # Veritabanına bağlan ve kaydet
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO movies (year, title) VALUES (?, ?)", (year_int, title)
    )
    conn.commit() 
    new_id = cur.lastrowid # ID numarasını al
    conn.close()

    # İşlem başarılıysa eklenen filmi ve 201 kodunu geri dön
    return jsonify({"id": new_id, "year": year_int, "title": title}), 201

# Görev 13: Query param ile film silme
@app.route("/movies", methods=["DELETE"])
def delete_movies_by_query():
    # ?year= değerini al
    year = request.args.get("year")
    
    # Yıl belirtilmemişse işlemi reddet
    if year is None:
        return jsonify({"error": "'year' query parametresi zorunludur."}), 400

    # Değer sayı mı 
    try:
        year_int = int(year)
    except ValueError:
        return jsonify({"error": "'year' sayisal bir deger olmalidir."}), 400

    conn = get_connection()

    # Hangi filmler silinecek
    to_delete = conn.execute(
        "SELECT title FROM movies WHERE year = ?", (year_int,)
    ).fetchall()
    deleted_titles = [row["title"] for row in to_delete]

    # Sil
    conn.execute("DELETE FROM movies WHERE year = ?", (year_int,))
    conn.commit()
    conn.close()

    # Hiç film bulunamadıysa
    if not deleted_titles:
        return jsonify({"message": f"{year_int} yilina ait film bulunamadi."}), 404

    # Başarıyla silindiyse
    return jsonify({
        "message": f"{len(deleted_titles)} film silindi.",
        "year": year_int,
        "deleted_titles": deleted_titles
    })

# Görev 14: Path param ile film silme
@app.route("/movies/<int:year>", methods=["DELETE"])
def delete_movies_by_path(year):
    conn = get_connection()

    # Hangi filmler silinecek
    to_delete = conn.execute(
        "SELECT title FROM movies WHERE year = ?", (year,)
    ).fetchall()
    deleted_titles = [row["title"] for row in to_delete]

    # Sil
    conn.execute("DELETE FROM movies WHERE year = ?", (year,))
    conn.commit()
    conn.close()

    # Hiç film bulunamadıysa
    if not deleted_titles:
        return jsonify({"message": f"{year} yilina ait film bulunamadi."}), 404

    # Başarıyla silindiyse
    return jsonify({
        "message": f"{len(deleted_titles)} film silindi.",
        "year": year,
        "deleted_titles": deleted_titles
    })

# Görev 15: Film ara
@app.route("/search", methods=["GET"])
def search_movies():
    # Aranacak kelimeyi al
    title = request.args.get("title", "")

    conn = get_connection()
    # LIKE ve % ile kısmi metin araması yap
    rows = conn.execute(
        "SELECT id, year, title FROM movies WHERE title LIKE ? ORDER BY year ASC",
        (f"%{title}%",),
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# Görev 21: Film güncelle
@app.route("/movies", methods=["PUT"])
def update_movie():
    data = request.get_json(silent=True)
    if not data or "id" not in data:
        return jsonify({"error": "Guncelleme icin 'id' alani zorunludur."}), 400

    movie_id = data.get("id")
    year = data.get("year")
    title = data.get("title")

    if year is None or not title:
        return jsonify({"error": "'year' ve 'title' alanlari zorunludur."}), 400

    conn = get_connection()

    # Film gercekten var mi
    existing = conn.execute(
        "SELECT id FROM movies WHERE id = ?", (movie_id,)
    ).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": f"id={movie_id} ile film bulunamadi."}), 404

    conn.execute(
        "UPDATE movies SET year = ?, title = ? WHERE id = ?",
        (year, title, movie_id),
    )
    conn.commit()
    conn.close()

    return jsonify({"id": movie_id, "year": year, "title": title})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)