# TTG Staj Projesi

Bu depo, staj sürecinde verilen görevlerin çözümlerini içerir.

Şu an **Python temelleri** ve **Flask + SQLite REST API** bölümleri
tamamlandı. React frontend bölümü eklendiğinde bu dosya tekrar
güncellenecek.

## Klasör Yapısı

```
python_basics/   -> Görev 2-7: sayı filtreleme, faktöriyel, regex'ler, tire ekleme
backend/          -> Görev 8-15: Flask + SQLite REST API
```

## Python Görevleri Nasıl Çalıştırılır

```bash
cd python_basics
python 02_sayi_filtreleme.py
python 03_faktoriyel.py
python 04_parola_dogrulama.py
python 05_parola_regex.py
python 06_isim_regex.py
python 07_tire_ekleme.py
```

### Görevlerin İçeriği

| Dosya | Görev |
|---|---|
| `02_sayi_filtreleme.py` | 2000-3200 arasında 7'ye bölünen, 5'in katı olmayan sayıları bulur |
| `03_faktoriyel.py` | Faktöriyeli hem döngü hem recursive ile hesaplar |
| `04_parola_dogrulama.py` | Parola kurallarını manuel mantıkla kontrol eder |
| `05_parola_regex.py` | Aynı kontrolü tek bir regex ile yapar |
| `06_isim_regex.py` | İsim + göbek adı (opsiyonel) + SOYİSİM formatını regex ile doğrular |
| `07_tire_ekleme.py` | Ardışık iki tek rakamın arasına `-` ekler |

## Backend (Flask + SQLite) Nasıl Çalıştırılır

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
python app.py
```

Sunucu `http://127.0.0.1:5000` adresinde çalışır. İlk çalıştırmada
`movies.db` dosyası otomatik oluşturulur (veritabanı boş başlar, kayıtlar
`POST /movies` ile eklenir).

### Endpoint'ler

| Method | Endpoint | Açıklama |
|---|---|---|
| GET | `/` | Tüm filmleri (year, title) year'a göre artan sıralı döndürür |
| GET | `/movies?year=1983` | Belirli yıla ait filmleri döndürür |
| POST | `/movies` | Yeni film ekler (body: `year`, `title`) |
| DELETE | `/movies?year=2023` | Query param ile o yıldaki filmleri siler |
| DELETE | `/movies/2023` | Path param ile o yıldaki filmleri siler |
| GET | `/search?title=matrix` | Title alanında LIKE ile arama yapar |

Silme endpoint'leri, silinen filmlerin isimlerini de (`deleted_titles`)
cevapla birlikte döner.

### Postman ile Test

`backend/postman_collection.json` dosyası Postman'e **File > Import** ile
eklenip her endpoint tek tek test edilebilir.

### Notlar

- Tüm SQL sorguları parametreli (`?` placeholder) yazıldı, SQL injection
  riski yok.
- Eksik/geçersiz istekler (boş alan, olmayan kayıt, yanlış tip) uygun HTTP
  status kodlarıyla (400/404) ve açıklayıcı JSON mesajıyla dönüyor.
- `venv/`, `movies.db`, `__pycache__/` gibi dosyalar `.gitignore` ile
  hariç tutuldu, GitHub'a yüklenmedi — herkes kendi ortamında
  `pip install -r requirements.txt` ve `python app.py` ile aynı ortamı
  kurabilir.

## Genel Notlar

- Tüm scriptler `python3 <dosya>.py` (veya Windows'ta `python <dosya>.py`)
  ile terminalden çalıştırılıp test edildi.
- Backend'deki tüm endpoint'ler Postman ile ayrı ayrı test edildi.