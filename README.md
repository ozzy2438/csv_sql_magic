# CSV'den PostgreSQL'e Veri Aktarma Aracı

Bu Python scripti, CSV dosyalarını PostgreSQL veritabanına aktarmanızı sağlar.

## Özellikler

- CSV dosyasını otomatik olarak okur
- Veritabanı tablosunu otomatik olarak oluşturur
- Veri tiplerini otomatik olarak eşleştirir
- Güvenli bağlantı yönetimi için .env desteği

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyasını düzenleyin:
```
DB_NAME=veritabani_adi
DB_USER=kullanici_adi
DB_PASSWORD=sifre
DB_HOST=localhost
DB_PORT=5432
```

## Kullanım

```bash
python csv_to_sql.py <csv_dosyası> <tablo_adı>
```

Örnek:
```bash
python csv_to_sql.py veriler.csv musteri_tablosu
```

## Notlar

- CSV dosyanızın ilk satırı sütun başlıklarını içermelidir
- PostgreSQL veritabanınızın çalışır durumda olduğundan emin olun
- Veritabanı kullanıcınızın tablo oluşturma ve veri ekleme yetkilerine sahip olduğundan emin olun