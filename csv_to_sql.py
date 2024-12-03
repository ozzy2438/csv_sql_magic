import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

def connect_to_db():
    """Veritabanı bağlantısını oluşturur"""
    load_dotenv()  # .env dosyasından çevresel değişkenleri yükle
    
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn

def create_table(conn, table_name, df):
    """DataFrame'e göre tablo oluşturur"""
    with conn.cursor() as cur:
        # DataFrame sütun tiplerini PostgreSQL tiplerine dönüştür
        type_mapping = {
            'int64': 'INTEGER',
            'float64': 'FLOAT',
            'object': 'TEXT',
            'datetime64[ns]': 'TIMESTAMP'
        }
        
        columns = []
        for column, dtype in df.dtypes.items():
            sql_type = type_mapping.get(str(dtype), 'TEXT')
            columns.append(f'"{column}" {sql_type}')
        
        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join([sql.SQL(col) for col in columns])
        )
        
        cur.execute(create_table_query)
        conn.commit()

def insert_data(conn, table_name, df):
    """DataFrame verilerini tabloya ekler"""
    with conn.cursor() as cur:
        # Sütun isimlerini hazırla
        columns = [sql.Identifier(col) for col in df.columns]
        
        # INSERT sorgusunu hazırla
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(columns),
            sql.SQL(', ').join([sql.Placeholder() for _ in columns])
        )
        
        # Verileri ekle
        for _, row in df.iterrows():
            cur.execute(insert_query, list(row))
        
        conn.commit()

def main(csv_file, table_name):
    """Ana fonksiyon"""
    try:
        # CSV dosyasını oku
        df = pd.read_csv(csv_file)
        print(f"CSV dosyası başarıyla okundu: {len(df)} satır")
        
        # Veritabanına bağlan
        conn = connect_to_db()
        print("Veritabanına bağlantı başarılı")
        
        # Tabloyu oluştur
        create_table(conn, table_name, df)
        print(f"'{table_name}' tablosu oluşturuldu")
        
        # Verileri ekle
        insert_data(conn, table_name, df)
        print(f"Veriler '{table_name}' tablosuna başarıyla eklendi")
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Veritabanı bağlantısı kapatıldı")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Kullanım: python csv_to_sql.py <csv_dosyası> <tablo_adı>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    table_name = sys.argv[2]
    main(csv_file, table_name) 