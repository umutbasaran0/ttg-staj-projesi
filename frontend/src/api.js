import axios from "axios";

// Flask backend'in adresi
const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

// Gorev 17-18: Tum filmleri getirir
export const getMovies = () => api.get("/");

// Gorev 19: Baslikta arama yapar 
export const searchMovies = (title) =>
  api.get("/search", { params: { title } });

// Gorev 20: Yeni film ekler
export const addMovie = (movie) => api.post("/movies", movie);

// Gorev 21: Mevcut filmi gunceller
export const updateMovie = (movie) => api.put("/movies", movie);

export default api;