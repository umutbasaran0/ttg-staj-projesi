import { DatePicker } from "antd";

function App() {
  return (
    <div style={{ padding: 24 }}>
      <h1>Film Yönetimi</h1>
      <DatePicker picker="year" placeholder="Yil seçin" />
    </div>
  );
}

export default App;