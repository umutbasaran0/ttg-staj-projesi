import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const getMovies = () => api.get("/");

export const searchMovies = (title) =>
  api.get("/search", { params: { title } });

export const addMovie = (movie) => api.post("/movies", movie);

export const updateMovie = (movie) => api.put("/movies", movie);

export default api;