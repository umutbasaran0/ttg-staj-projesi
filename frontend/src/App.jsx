import { useState } from "react";
import { DatePicker, Table, Button, Input, Modal, Form, message, Space } from "antd";
import { getMovies, searchMovies, addMovie, updateMovie } from "./api";
import dayjs from "dayjs";

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingMovie, setEditingMovie] = useState(null);
  const [form] = Form.useForm();

  const mapToTableData = (data) =>
    data.map((movie, index) => ({ ...movie, key: movie.id ?? index }));

  const handleLoad = () => {
    setLoading(true);
    getMovies()
      .then((res) => setMovies(mapToTableData(res.data)))
      .catch((err) => console.error("Filmler yuklenirken hata:", err))
      .finally(() => setLoading(false));
  };

  const handleSearch = (title) => {
    if (!title) {
      handleLoad();
      return;
    }
    setLoading(true);
    searchMovies(title)
      .then((res) => setMovies(mapToTableData(res.data)))
      .catch((err) => console.error("Arama sirasinda hata:", err))
      .finally(() => setLoading(false));
  };

  const openAddModal = () => {
    setEditingMovie(null);
    form.resetFields();
    setIsModalOpen(true);
  };

  const openEditModal = (movie) => {
    setEditingMovie(movie);
    form.setFieldsValue({
      title: movie.title,
      year: dayjs(String(movie.year), "YYYY"),
    });
    setIsModalOpen(true);
  };

  const handleModalOk = () => {
    form
      .validateFields()
      .then((values) => {
        const payload = {
          title: values.title,
          year: values.year.year(),
        };

        if (editingMovie) {
          return updateMovie({ id: editingMovie.id, ...payload });
        }
        return addMovie(payload);
      })
      .then(() => {
        message.success(editingMovie ? "Film guncellendi." : "Film eklendi.");
        setIsModalOpen(false);
        handleLoad();
      })
      .catch((err) => {
        if (err?.errorFields) return;
        console.error("Islem sirasinda hata:", err);
        message.error("Bir hata olustu.");
      });
  };

  const columns = [
    { title: "Yıl", dataIndex: "year", key: "year" },
    { title: "Başlık", dataIndex: "title", key: "title" },
    {
      title: "İşlemler",
      key: "actions",
      render: (_, record) => (
        <Space>
          <Button size="small" onClick={() => openEditModal(record)}>
            Güncelle
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h1>Film Yönetimi</h1>

      <div style={{ marginBottom: 16, display: "flex", gap: 8 }}>
        <Button onClick={handleLoad} loading={loading}>
          Yükle
        </Button>
        <Input.Search
          placeholder="Film adı ile ara..."
          onSearch={handleSearch}
          allowClear
          style={{ width: 250 }}
        />
        <Button type="primary" onClick={openAddModal}>
          Ekle
        </Button>
      </div>

      <Table columns={columns} dataSource={movies} loading={loading} />

      <Modal
        title={editingMovie ? "Filmi Güncelle" : "Yeni Film Ekle"}
        open={isModalOpen}
        onOk={handleModalOk}
        onCancel={() => setIsModalOpen(false)}
        okText={editingMovie ? "Güncelle" : "Ekle"}
        cancelText="Vazgeç"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="title"
            label="Film Adı"
            rules={[{ required: true, message: "Film adı zorunludur." }]}
          >
            <Input placeholder />
          </Form.Item>
          <Form.Item
            name="year"
            label="Yıl"
            rules={[{ required: true, message: "Yıl seçmelisiniz." }]}
          >
            <DatePicker picker="year" style={{ width: "100%" }} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

export default App;