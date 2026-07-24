import { useState } from "react";
import { DatePicker, Table, Button } from "antd";
import { getMovies } from "./api";

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleLoad = () => {
    setLoading(true);
    getMovies()
      .then((res) => {
        const data = res.data.map((movie, index) => ({
          ...movie,
          key: index,
        }));
        setMovies(data);
      })
      .catch((err) => console.error("Filmler yuklenirken hata:", err))
      .finally(() => setLoading(false));
  };

  const columns = [
    { title: "Yıl", dataIndex: "year", key: "year" },
    { title: "Başlık", dataIndex: "title", key: "title" },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h1>Film Yönetimi</h1>
      <DatePicker picker="year" placeholder="Yıl seçin" style={{ marginBottom: 16 }} />
      <div style={{ marginBottom: 16 }}>
        <Button onClick={handleLoad} loading={loading}>
          Yükle
        </Button>
      </div>
      <Table columns={columns} dataSource={movies} />
    </div>
  );
}

export default App;