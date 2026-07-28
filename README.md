# TTG Staj Projesi

Bu depo, staj sürecinde verilen görevlerin çözümlerini içerir.

Proje üç bölümden oluşuyor, üçü de tamamlandı: **Python temelleri**,
**Flask + SQLite REST API** ve **React + Ant Design frontend**.

## Klasör Yapısı

```
python_basics/   -> Görev 2-7: sayı filtreleme, faktöriyel, regex'ler, tire ekleme
backend/         -> Görev 8-15, 21: Flask + SQLite REST API
frontend/        -> Görev 16-22: React + Vite + Ant Design
fastapi_backend/ -> Görev 23: Ayni API'nin FastAPI ile yeniden yazilmis hali
go_backend/      -> Görev 24: Ayni API'nin Go ile yeniden yazilmis hali
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
`movies.db` dosyası otomatik oluşturulur.

### Endpoint'ler

| Method | Endpoint | Açıklama |
|---|---|---|
| GET | `/` | Tüm filmleri (id, year, title) year'a göre artan sıralı döndürür |
| GET | `/movies?year=1983` | Belirli yıla ait filmleri döndürür |
| POST | `/movies` | Yeni film ekler (body: `year`, `title`) |
| PUT | `/movies` | Mevcut filmi günceller (body: `id`, `year`, `title`) |
| DELETE | `/movies?year=2023` | Query param ile o yıldaki filmleri siler |
| DELETE | `/movies/2023` | Path param ile o yıldaki filmleri siler |
| GET | `/search?title=matrix` | Title alanında LIKE ile arama yapar |

Silme endpoint'leri, silinen filmlerin isimlerini de (`deleted_titles`)
cevapla birlikte döner. `flask-cors` ile React uygulamasının farklı
porttan (5173) istek atabilmesi sağlandı.

### Postman ile Test

`backend/postman_collection.json` dosyası Postman'e **File > Import** ile
eklenip her endpoint tek tek test edilebilir.

### Notlar

- Tüm SQL sorguları parametreli (`?` placeholder) yazıldı, SQL injection
  riski yok.
- Eksik/geçersiz istekler (boş alan, olmayan kayıt, yanlış tip) uygun HTTP
  status kodlarıyla (400/404) ve açıklayıcı JSON mesajıyla dönüyor.
- `venv/`, `movies.db`, `__pycache__/` gibi dosyalar `.gitignore` ile
  hariç tutuldu, GitHub'a yüklenmedi.

## Frontend (React + Vite + Ant Design) Nasıl Çalıştırılır

Backend'in ayrı bir terminalde çalışıyor olması gerekir (yukarıdaki
adımlarla `http://127.0.0.1:5000` üzerinde ayakta olmalı).

```bash
cd frontend
npm install
npm run dev
```

Uygulama `http://localhost:5173` adresinde açılır.

### Özellikler

| Özellik | Açıklama |
|---|---|
| DatePicker | Yıl seçimi için Ant Design DatePicker bileşeni kullanıldı |
| Yükle | Sayfa boş açılır, "Yükle" butonuna basınca `GET /` ile filmler çekilir |
| Arama | Ant Design Search Input ile `GET /search?title=X` (SQL LIKE) üzerinden arama yapılır |
| Ekle | Modal içinde form doldurulup `POST /movies` ile yeni film kaydedilir |
| Güncelle | Mevcut film bilgileri formda gösterilip `PUT /movies` ile güncellenir |
| Dışa Aktar | Tablo verisi CSV veya Excel (.xlsx) olarak indirilebilir |

### Notlar

- API çağrıları `src/api.js` içinde tek bir yerden yönetiliyor (axios).
- Hatalı işlemlerde (`try/catch` benzeri `.catch(...)`) kullanıcıya Ant
  Design `message` bileşeniyle bilgilendirme yapılıyor, sayfa çökmüyor.
- `node_modules/` ve `dist/` `.gitignore` ile hariç tutuldu, GitHub'a
  yüklenmedi — `npm install` ile herkes kendi ortamını kurabilir.


## Ek Çalışmalar

Aynı Movies API, iki farklı teknolojiyle yeniden yazıldı. Her ikisi de
Flask sürümüyle birebir aynı endpoint yapısını kullanıyor, bu sayede
React frontend'i sadece `baseURL` değiştirilerek her üçüyle de
çalışacak şekilde tasarlandı.
 
### FastAPI (Görev 23)
 
Aynı REST API'nin FastAPI ile yeniden yazılmış hali `fastapi_backend/`
klasöründe. Çalıştırmak için:

```bash
cd fastapi_backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
 
Sunucu `http://127.0.0.1:8000` adresinde çalışır.
 
Otomatik oluşan dokümantasyon (Swagger UI): `http://127.0.0.1:8000/docs`
— her endpoint buradan "Try it out" ile Postman'e gerek kalmadan test
edilebilir.

### Go (Görev 24)
 
Aynı REST API'nin Go (yalnızca standart kütüphane kullanılarak)
yeniden yazılmış hali `go_backend/` klasöründe. Çalıştırmak için:
 
```bash
cd go_backend
go run main.go
```
 
Sunucu `http://127.0.0.1:8002` adresinde çalışır ve başlangıçta 5 örnek
film (`seedData`) ile otomatik doluyor, ekstra veri eklemeye gerek kalmadan
test edilebilir.

Derleyip `.exe` olarak da çalıştırılabilir:
```bash
go build -o movies-api.exe main.go
.\movies-api.exe
```

Her iki backend de Postman ile uçtan uca test edildi (GET, POST, PUT,
DELETE, hata durumları). 

## Genel Notlar

- Tüm Python scriptleri ve backend endpoint'leri Postman ile ayrı ayrı
  test edildi.
- Frontend, backend ile birlikte çalıştırılıp tüm özellikler (yükleme,
  arama, ekleme, güncelleme, dışa aktarma) uçtan uca test edildi.
- FastAPI ve Go backend'leri Postman ile ayrı ayrı test edildi; endpoint 
  yapıları Flask sürümüyle birebir aynı olduğu için React frontend'i baseURL 
  değiştirilerek bunlarla da çalışacak şekilde tasarlandı.