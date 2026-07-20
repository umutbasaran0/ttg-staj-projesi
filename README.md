# TTG Staj Projesi

Bu depo, staj sürecinde verilen görevlerin çözümlerini içerir.

Şu an sadece **Python temelleri** bölümü tamamlandı, Flask + SQLite API ve React frontend bölümleri de eklenip bu dosya güncellenecek.

## Klasör Yapısı

```
python_basics/   -> Görev 2-7: sayı filtreleme, faktöriyel, regex'ler, tire ekleme
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

## Görevlerin İçeriği

| Dosya | Görev |
|---|---|
| `02_sayi_filtreleme.py` | 2000-3200 arasında 7'ye bölünen, 5'in katı olmayan sayıları bulur |
| `03_faktoriyel.py` | Faktöriyeli hem döngü hem recursive ile hesaplar |
| `04_parola_dogrulama.py` | Parola kurallarını manuel mantıkla kontrol eder |
| `05_parola_regex.py` | Aynı kontrolü tek bir regex ile yapar |
| `06_isim_regex.py` | İsim + göbek adı (opsiyonel) + SOYİSİM formatını regex ile doğrular |
| `07_tire_ekleme.py` | Ardışık iki tek rakamın arasına `-` ekler |

## Notlar

- Tüm scriptler `python3 <dosya>.py` (veya Windows'ta `python <dosya>.py`)
  ile terminalden çalıştırılıp test edildi.