# 🧠 FileSynapse AI - Akıllı Dosya Düzenleme Sistemi

## 📋 İçindekiler
- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Teknik Detaylar](#-teknik-detaylar)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

## 🎯 Proje Hakkında
FileSynapse AI, yapay zeka destekli akıllı bir klasör düzenleme aracıdır. Dosyalarınızı içeriklerine ve türlerine göre otomatik olarak kategorize eder ve düzenler. Özellikle dağınık disklerinizi ve proje klasörlerinizi düzenlemek için tasarlanmıştır.

### 📌 Gerçek Dünya Kullanım Senaryoları

#### 1. Disk Düzenleme
```
D:/
├── Downloads/
│   ├── invoice.pdf
│   ├── project.zip
│   └── photo.jpg
├── Documents/
│   ├── report.docx
│   └── presentation.pptx
└── Projects/
    ├── design1.psd
    └── code.py
```

FileSynapse AI bu yapıyı şöyle düzenler:
```
D:/
├── Belgeler/
│   ├── Faturalar/
│   │   └── invoice.pdf
│   ├── Raporlar/
│   │   └── report.docx
│   └── Sunumlar/
│       └── presentation.pptx
├── Projeler/
│   ├── WebProjesi/
│   │   ├── design1.psd
│   │   └── code.py
│   └── Arşiv/
│       └── project.zip
└── Medya/
    └── Fotoğraflar/
        └── photo.jpg
```

#### 2. Tasarım Projeleri Düzenleme
```
Designs/
├── logo_v1.psd
├── logo_v2.psd
├── banner_final.psd
├── banner_draft.psd
├── social_media_icons.ai
└── brand_guidelines.pdf
```

FileSynapse AI bu yapıyı şöyle düzenler:
```
Designs/
├── Logo/
│   ├── Versiyonlar/
│   │   ├── logo_v1.psd
│   │   └── logo_v2.psd
├── Banner/
│   ├── Final/
│   │   └── banner_final.psd
│   └── Taslaklar/
│       └── banner_draft.psd
├── Assets/
│   └── social_media_icons.ai
└── Dokümanlar/
    └── brand_guidelines.pdf
```

## ✨ Özellikler

### 🔍 1. Dosya Analizi
- Klasördeki dosyaları ve klasörleri tarar (PDF, PNG, EXE, TXT, vb.)
- Dosya boyutu, uzantı, oluşturulma/değiştirilme tarihi gibi meta verileri çıkarır
- AI model ile içeriğe göre sınıflandırma (örn. PDF'nin içinde "Fatura" geçiyorsa, "Faturalar" klasörüne taşı)
- Dosya isimlerindeki versiyon numaralarını ve tarihleri analiz eder (v1, v2, final, draft vb.)
- Benzer dosyaları gruplar (örn. aynı projeye ait tasarım dosyaları)

### 🧠 2. AI Destekli Kategorilendirme
- Dosya adları ve içeriklerine göre kategoriler tahmin eder:
  - Belgeler (CV, makale, fatura)
  - Medya (fotoğraf, video, müzik)
  - Programlar / Kurulum dosyaları
  - Kod dosyaları (proje klasörleri vb.)
  - Tasarım dosyaları (PSD, AI, Sketch vb.)
  - Proje versiyonları ve taslaklar
- Önceden eğitilmiş küçük bir model veya yerel ML algoritması kullanır
- Dosya içeriğini analiz ederek proje bazlı gruplandırma yapar

### 📁 3. Klasör Yapısı Önerisi ve Oluşturma
- Akıllı klasör yapısı önerileri
- Otomatik klasör oluşturma ve dosya taşıma
- Kullanıcı onayı ile işlem yapma

### 🔁 4. Gerçek Zamanlı İzleme
- Belirli klasörleri otomatik izleme
- Yeni dosyaları anlık kategorilendirme
- Arka plan işlemleri

### ⚙️ 5. Kural Tabanlı Özelleştirme
- Özel kural tanımlama
- Dosya adı ve uzantı bazlı filtreleme
- AI sonuçlarını özelleştirme

### 🧾 6. İşlem Geçmişi ve Geri Alma
- Detaylı işlem logları
- Tek tıkla geri alma
- İşlem geçmişi görüntüleme

### 🌐 7. Çok Dilli Destek
- İngilizce ve Türkçe arayüz
- Çok dilli içerik analizi
- Dil bazlı kategorilendirme

## 💻 Kurulum

### Gereksinimler
- Python 3.8+
- Node.js 14+ (Electron.js versiyonu için)
- 4GB+ RAM
- 500MB disk alanı

### Kurulum Adımları
```bash
# Python versiyonu için
pip install -r requirements.txt

# Electron.js versiyonu için
npm install
```

## 🚀 Kullanım

### Hızlı Başlangıç
1. FileSynapse AI'ı başlatın
2. Düzenlemek istediğiniz klasörü seçin (örn. D: sürücüsü veya Designs klasörü)
3. AI analizini başlatın
4. Önerilen düzenlemeleri inceleyin
5. Onaylayın ve uygulayın

### Örnek Kullanım Senaryoları

#### 1. Tüm Diski Düzenleme
```bash
# D: sürücüsünü düzenle
filesynapse --path D:/ --mode full-disk

# Sadece belirli klasörleri düzenle
filesynapse --path D:/ --include "Downloads,Documents,Projects"
```

#### 2. Tasarım Projelerini Düzenleme
```bash
# Tasarım klasörünü düzenle
filesynapse --path Designs/ --mode design-projects

# Versiyon kontrolü ile düzenle
filesynapse --path Designs/ --version-control
```

#### 3. Özel Kurallar ile Düzenleme
```bash
# Özel kural dosyası ile düzenle
filesynapse --path D:/ --rules custom_rules.json

# Belirli dosya türlerini düzenle
filesynapse --path D:/ --file-types "psd,ai,sketch"
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- Python / Electron.js
- TensorFlow / PyTorch
- SQLite (işlem geçmişi için)
- PyQt5 / React (UI için)
- Fuzzy Matching (benzer dosya isimlerini bulmak için)
- NLP (dosya içeriği analizi için)

### AI Modeli
- Önceden eğitilmiş BERT tabanlı model
- TF-IDF ve küçük dil modeli
- Sürekli öğrenme ve güncelleme
- Dosya ismi ve içerik analizi
- Proje bazlı gruplandırma algoritması

## 🤝 Katkıda Bulunma
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🎨 Kullanıcı Arayüzü (UI)

### Ana Ekran
```
+---------------------------------------------------------+
|               FileSynapse AI - Düzenleyici              |
+---------------------------------------------------------+

[📁 Klasör Seçin]  [Başlat 🚀]

-----------------------------------------------------------
🔍 Taranan Dosya Türleri: PDF (5), JPG (10), EXE (1) ...
🧠 AI Tahmini: Belgeler (PDF), Görseller (JPG), Uygulama (EXE)

[📂 Oluşturulacak klasör yapısı görüntüle 👁️]
   - Belgeler/
   - Fotoğraflar/
   - Yazılımlar/

[⚙️ Kurallarım]  [📜 Geçmiş]  [🌐 Dil: Türkçe/English]

[🧪 Test Et] [✅ Onayla ve Uygula]
```

### Özelleştirme Panelleri
- **Kurallar Paneli**: Özel klasör oluşturma kuralları
- **Geçmiş Paneli**: İşlem kayıtları ve geri alma seçenekleri
- **Ayarlar Paneli**: Uygulama tercihleri ve dil seçenekleri