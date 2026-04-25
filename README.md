# 📊 Kişisel Finans Yönetimi Uygulaması

Bu proje, gelir ve gider kayıtlarının tutulması, listelenmesi, analiz edilmesi ve grafiklerle görselleştirilmesi amacıyla geliştirilmiş bir kişisel finans yönetimi uygulamasıdır.

Uygulama Python ve Streamlit kullanılarak hazırlanmıştır. Veriler SQLite veritabanında depolanır. Kullanıcı gelir ve gider kayıtları ekleyebilir, kayıtları görüntüleyebilir, silebilir, filtreleyebilir ve analiz sonuçlarını grafikler üzerinden inceleyebilir.

---

## 🎯 Proje Amacı

Bu projenin amacı, kişisel finans takibini daha düzenli hale getiren basit ve anlaşılır bir uygulama geliştirmektir.

Uygulama ile:
- Gelir ve gider kayıtları tutulabilir
- Finansal durum özetlenebilir
- Harcamalar kategori bazında incelenebilir
- Gelir ve gider değişimleri grafiklerle takip edilebilir
- Kayıtlar dışa aktarılabilir

---

## 🚀 Özellikler

### Veri İşlemleri
- Gelir kaydı ekleme
- Gider kaydı ekleme
- Kategori seçimi
- Tarih seçimi
- Not ekleme
- Kayıt silme
- Kayıtları tablo halinde görüntüleme

### Analiz Özellikleri
- Toplam gelir hesaplama
- Toplam gider hesaplama
- Net bakiye hesaplama
- Kayıt sayısı gösterme
- En fazla harcama yapılan kategoriyi gösterme
- Ortalama gelir hesaplama
- Ortalama gider hesaplama
- Son 5 kaydı görüntüleme

### Grafikler
- Aylık gelir / gider grafiği
- Finansal değişim grafiği
- Gider kategorileri dağılım grafiği
- Gelir kategorileri dağılım grafiği
- Kategoriye göre toplam tutar grafiği

### Filtreleme ve Dışa Aktarma
- İşlem türüne göre filtreleme
- Tarih aralığına göre filtreleme
- Kategoriye göre arama
- Kayıtları CSV olarak indirme

---

## 🛠 Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|---|---|
| Python | Uygulamanın temel programlama dili |
| Streamlit | Web arayüzünün oluşturulması |
| SQLite | Verilerin depolanması |
| Pandas | Verilerin işlenmesi ve tablo yapısı |
| Plotly | Grafiklerin oluşturulması |

---

## 📁 Proje Dosyaları

| Dosya / Klasör | Açıklama |
|---|---|
| app.py | Ana uygulama dosyası |
| database.py | Veritabanı işlemleri için yardımcı dosya |
| requirements.txt | Gerekli Python paketleri |
| README.md | Proje açıklama dosyası |
| LICENSE | Proje lisans dosyası |

---

## ⚙️ Kurulum

Projeyi çalıştırmak için önce gerekli paketler kurulmalıdır:

```bash
pip install -r requirements.txt
```

Daha sonra uygulama şu komutla çalıştırılır:

```bash
streamlit run app.py
```

---

## 📝 Not

Uygulama ilk çalıştırıldığında veritabanı otomatik olarak oluşturulur.

SQLite, Python ile birlikte geldiği için `requirements.txt` dosyasına ayrıca eklenmemiştir.

---

## 📌 Kullanım

1. Uygulama çalıştırılır.
2. Menüden "İşlem Ekle" sayfasına gidilir.
3. Gelir veya gider bilgileri girilir.
4. Kayıtlar "Veri Listesi" sayfasında görüntülenebilir.
5. "Analiz" sayfasında grafikler ve özet bilgiler incelenebilir.
6. İstenirse kayıtlar CSV dosyası olarak indirilebilir.

---

## 👤 Geliştirici

Uygar Kutluğ
