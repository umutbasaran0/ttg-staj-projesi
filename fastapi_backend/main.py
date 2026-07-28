from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_connection, init_db

app = FastAPI(title="Movies API - FastAPI")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Film ekleme modeli
class MovieCreate(BaseModel):
    year: int
    title: str

# Güncelleme modeli
class MovieUpdate(BaseModel):
    id: int
    year: int
    title: str


@app.on_event("startup")
def on_startup():
    init_db()

# Filmleri listele
@app.get("/")
def list_movies():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, year, title FROM movies ORDER BY year ASC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Yıla göre listele
@app.get("/movies")
def get_movies(year: Optional[int] = None):
    conn = get_connection()

    if year is not None:
        rows = conn.execute(
            "SELECT id, year, title FROM movies WHERE year = ? ORDER BY year ASC",
            (year,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, year, title FROM movies ORDER BY year ASC"
        ).fetchall()

    conn.close()
    return [dict(row) for row in rows]

# Yeni film ekle
@app.post("/movies", status_code=201)
def add_movie(movie: MovieCreate):
    if not movie.title:
        raise HTTPException(status_code=400, detail="'title' bos olamaz.")

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO movies (year, title) VALUES (?, ?)", (movie.year, movie.title)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": new_id, "year": movie.year, "title": movie.title}

# Filmi güncelle
@app.put("/movies")
def update_movie(movie: MovieUpdate):
    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM movies WHERE id = ?", (movie.id,)
    ).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail=f"id={movie.id} ile film bulunamadi.")

    conn.execute(
        "UPDATE movies SET year = ?, title = ? WHERE id = ?",
        (movie.year, movie.title, movie.id),
    )
    conn.commit()
    conn.close()

    return {"id": movie.id, "year": movie.year, "title": movie.title}

# Query ile film silme
@app.delete("/movies")
def delete_movies_by_query(year: int):
    conn = get_connection()

    to_delete = conn.execute(
        "SELECT title FROM movies WHERE year = ?", (year,)
    ).fetchall()
    deleted_titles = [row["title"] for row in to_delete]

    conn.execute("DELETE FROM movies WHERE year = ?", (year,))
    conn.commit()
    conn.close()

    if not deleted_titles:
        raise HTTPException(status_code=404, detail=f"{year} yilina ait film bulunamadi.")

    return {
        "message": f"{len(deleted_titles)} film silindi.",
        "year": year,
        "deleted_titles": deleted_titles,
    }

# Path ile film silme
@app.delete("/movies/{year}")
def delete_movies_by_path(year: int):
    conn = get_connection()

    to_delete = conn.execute(
        "SELECT title FROM movies WHERE year = ?", (year,)
    ).fetchall()
    deleted_titles = [row["title"] for row in to_delete]

    conn.execute("DELETE FROM movies WHERE year = ?", (year,))
    conn.commit()
    conn.close()

    if not deleted_titles:
        raise HTTPException(status_code=404, detail=f"{year} yilina ait film bulunamadi.")

    return {
        "message": f"{len(deleted_titles)} film silindi.",
        "year": year,
        "deleted_titles": deleted_titles,
    }
# Film adına göre arama yapma
@app.get("/search")
def search_movies(title: str = ""):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, year, title FROM movies WHERE title LIKE ? ORDER BY year ASC",
        (f"%{title}%",),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]