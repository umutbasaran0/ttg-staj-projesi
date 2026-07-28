package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sort"
	"strconv"
	"strings"
	"sync"
)

// Film verilerinin yapısını belirten kalıp
type Movie struct {
	ID int `json:"id"`
	Year int `json:"year"`
	Title string `json:"title"`
}

// Global değişkenler
var (
	mu sync.Mutex
	movies []Movie
	nextID = 1
)

// Örnek veriler
func seedData() {
	sample := []Movie{
		{Year: 1983, Title: "Return of the Jedi"},
		{Year: 1994, Title: "The Shawshank Redemption"},
		{Year: 1999, Title: "The Matrix"},
		{Year: 2010, Title: "Inception"},
		{Year: 2019, Title: "Parasite"},
	}
	for _, m := range sample {
		m.ID = nextID
		nextID++
		movies = append(movies, m)
	}
}

// Verileri JSON formatına çeviren fonksiyon
func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

// JSON formatında hata mesajı dönen fonksiyon
func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]string{"error": message})
}

// CORS ayarları
func enableCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}
		next.ServeHTTP(w, r)
	})
}

// Filmleri listele
func listMovies(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	// Filmleri kopyala
	result := make([]Movie, len(movies))
	copy(result, movies)
	sort.Slice(result, func(i, j int) bool { return result[i].Year < result[j].Year })

	writeJSON(w, http.StatusOK, result)
}

// Yıla göre listele
func getMovies(w http.ResponseWriter, r *http.Request) {
	yearParam := r.URL.Query().Get("year")

	mu.Lock()
	defer mu.Unlock()

	if yearParam == "" {
		result := make([]Movie, len(movies))
		copy(result, movies)
		sort.Slice(result, func(i, j int) bool { return result[i].Year < result[j].Year })
		writeJSON(w, http.StatusOK, result)
		return
	}

	year, err := strconv.Atoi(yearParam)
	if err != nil {
		writeError(w, http.StatusBadRequest, "year sayisal bir deger olmalidir.")
		return
	}

	var result []Movie
	for _, m := range movies {
		if m.Year == year {
			result = append(result, m)
		}
	}
	if result == nil {
		result = []Movie{}
	}
	writeJSON(w, http.StatusOK, result)
}

// Yeni film ekle
func addMovie(w http.ResponseWriter, r *http.Request) {
	var input Movie
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		writeError(w, http.StatusBadRequest, "JSON govdesi bekleniyor.")
		return
	}
	if input.Title == "" {
		writeError(w, http.StatusBadRequest, "'title' alani zorunludur.")
		return
	}

	mu.Lock()
	input.ID = nextID
	nextID++
	movies = append(movies, input)
	mu.Unlock()

	writeJSON(w, http.StatusCreated, input)
}

// Filmi güncelle
func updateMovie(w http.ResponseWriter, r *http.Request) {
	var input Movie
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil || input.ID == 0 {
		writeError(w, http.StatusBadRequest, "Guncelleme icin 'id' alani zorunludur.")
		return
	}
	if input.Title == "" {
		writeError(w, http.StatusBadRequest, "'title' alani zorunludur.")
		return
	}

	mu.Lock()
	defer mu.Unlock()

	for i, m := range movies {
		if m.ID == input.ID {
			movies[i].Year = input.Year
			movies[i].Title = input.Title
			writeJSON(w, http.StatusOK, movies[i])
			return
		}
	}

	writeError(w, http.StatusNotFound, "boyle bir film bulunamadi.")
}

// Query ile film silme
func deleteMoviesByQuery(w http.ResponseWriter, r *http.Request) {
	yearParam := r.URL.Query().Get("year")
	if yearParam == "" {
		writeError(w, http.StatusBadRequest, "'year' query parametresi zorunludur.")
		return
	}
	year, err := strconv.Atoi(yearParam)
	if err != nil {
		writeError(w, http.StatusBadRequest, "'year' sayisal bir deger olmalidir.")
		return
	}

	deleteByYear(w, year)
}

// Path ile film silme
func deleteMoviesByPath(w http.ResponseWriter, r *http.Request) {
	yearParam := r.PathValue("year")
	year, err := strconv.Atoi(yearParam)
	if err != nil {
		writeError(w, http.StatusBadRequest, "yil sayisal bir deger olmalidir.")
		return
	}

	deleteByYear(w, year)
}

// Yıla göre film silme işlemi
func deleteByYear(w http.ResponseWriter, year int) {
	mu.Lock()
	defer mu.Unlock()

	var remaining []Movie
	var deletedTitles []string

	for _, m := range movies {
		if m.Year == year {
			deletedTitles = append(deletedTitles, m.Title)
		} else {
			remaining = append(remaining, m)
		}
	}
	movies = remaining

	if len(deletedTitles) == 0 {
		writeError(w, http.StatusNotFound, strconv.Itoa(year)+" yilina ait film bulunamadi.")
		return
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"message":        strconv.Itoa(len(deletedTitles)) + " film silindi.",
		"year":           year,
		"deleted_titles": deletedTitles,
	})
}

// Film adına göre arama yapma
func searchMovies(w http.ResponseWriter, r *http.Request) {
	title := strings.ToLower(r.URL.Query().Get("title"))

	mu.Lock()
	defer mu.Unlock()

	var result []Movie
	for _, m := range movies {
		if strings.Contains(strings.ToLower(m.Title), title) {
			result = append(result, m)
		}
	}
	if result == nil {
		result = []Movie{}
	}
	sort.Slice(result, func(i, j int) bool { return result[i].Year < result[j].Year })

	writeJSON(w, http.StatusOK, result)
}

func main() {
	seedData()

	mux := http.NewServeMux()
	mux.HandleFunc("GET /{$}", listMovies) 
	mux.HandleFunc("GET /movies", getMovies)
	mux.HandleFunc("POST /movies", addMovie)
	mux.HandleFunc("PUT /movies", updateMovie)
	mux.HandleFunc("DELETE /movies", deleteMoviesByQuery)
	mux.HandleFunc("DELETE /movies/{year}", deleteMoviesByPath)
	mux.HandleFunc("GET /search", searchMovies)

	log.Println("Sunucu http://127.0.0.1:8002 adresinde calisiyor")
	log.Fatal(http.ListenAndServe(":8002", enableCORS(mux)))
}