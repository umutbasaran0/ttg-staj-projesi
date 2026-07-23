import { useState, useEffect } from "react";
import { DatePicker, Table } from "antd";
import { getMovies } from "./api";

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    getMovies()
      .then((res) => {
        // Her satır için benzersiz bir key
        const data = res.data.map((movie, index) => ({
          ...movie,
          key: index,
        }));
        setMovies(data);
      })
      .catch((err) => console.error("Filmler yuklenirken hata:", err));
  }, []);

  const columns = [
    { title: "Yıl", dataIndex: "year", key: "year" },
    { title: "Başlık", dataIndex: "title", key: "title" },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h1>Film Yönetimi</h1>
      <DatePicker picker="year" placeholder="Yıl seçin" style={{ marginBottom: 16 }} />
      <Table columns={columns} dataSource={movies} />
    </div>
  );
}

export default App;