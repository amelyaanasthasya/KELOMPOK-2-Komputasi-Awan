# ANALISIS LENGKAP

## 1. Rekomendasi Deployment Model

Untuk Sistem Data Kependudukan ini, kami merekomendasikan **Hybrid Cloud**. **Private Cloud** yang dikontrol penuh oleh negara menjadi inti sistem untuk menyimpan data rahasia, sedangkan **Public Cloud** hanya dipakai untuk bagian depan yang tidak menyimpan data sensitif.

### - Pembagian Segmen

| Segmen | Lokasi | Komponen |
|---|---|---|
| **Private Cloud (inti)** | Data center milik/dikendalikan pemerintah | Database kependudukan (nama, NIK, alamat, biometrik), layanan verifikasi inti, dan manajemen kunci enkripsi |
| **Public Cloud (pendukung)** | Penyedia cloud komersial | Portal publik cek status, halaman statis, cache non-sensitif, antrean layanan saat lonjakan, dan monitoring |

Jadi data rahasia tetap berada di infrastruktur yang dikontrol penuh negara, sedangkan Public Cloud hanya dimanfaatkan untuk beban yang tidak menyentuh data mentah warga.

### - Alasan Berdasarkan Karakteristik NIST

**a. On-demand self-service**
Instansi seperti dukcapil daerah, kepolisian, dan bank harus bisa mengajukan akses dan mendapatkan API key sendiri tanpa menunggu proses manual dari pusat. Di Private Cloud, hal ini disediakan lewat portal internal dengan persetujuan dan verifikasi identitas instansi yang ketat, sehingga **kerahasiaan tetap terjaga**. Di Public Cloud, server tambahan untuk portal publik bisa dibuat otomatis, sehingga mendukung **skalabilitas**.

**b. Broad network access**
Ribuan instansi di berbagai daerah mengakses sistem dari jaringan dan perangkat yang berbeda-beda. Public Cloud memberi jangkauan luas untuk portal publik, jadi masyarakat bisa cek status lewat web maupun HP (**skalabilitas**). Sementara itu, akses ke data inti dibatasi lewat VPN/leased line, API gateway, dan mutual TLS (**kerahasiaan**).

**c. Resource pooling**
Public Cloud memakai model multi-tenant, yaitu server fisiknya dipakai bersama oleh banyak pelanggan. Ini efisien, tetapi tidak cocok untuk NIK dan data biometrik karena data warga berada di infrastruktur yang tidak sepenuhnya dikontrol negara dan berisiko melanggar UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (**kerahasiaan**). Karena itu, pooling di Private Cloud hanya dipakai antar instansi pemerintah, sedangkan pooling multi-tenant di Public Cloud hanya untuk komponen non-sensitif yang tetap bisa dialokasikan dengan efisien (**skalabilitas**).

**d. Rapid elasticity**
Ini alasan utama kenapa Private Cloud saja tidak cukup. Lonjakan akses saat pemilu dan pendaftaran sekolah tidak merata, dan jika semua berada di Private Cloud, pemerintah harus menyediakan kapasitas untuk beban puncak yang jarang terpakai (**skalabilitas**). Dengan Hybrid, lapisan depan seperti portal, cek status, antrean, dan cache otomatis di-scale-out ke Public Cloud saat lonjakan, sementara Private Cloud hanya menangani query inti yang sudah tersaring. Hasilnya sistem tidak down dan data rahasia tetap aman di dalam (**kerahasiaan**).

**e. Measured service**
Pemakaian sumber daya perlu diukur untuk menjatah kuota tiap instansi, misalnya bank yang melakukan verifikasi KYC dalam jumlah besar. Di Private Cloud, pengukuran dipakai untuk audit log siapa mengakses data siapa, yang penting untuk akuntabilitas UU PDP (**kerahasiaan**). Di Public Cloud, pengukuran dipakai untuk skema pay-per-use, sehingga pemerintah hanya membayar saat terjadi lonjakan (**skalabilitas**).

## 2. Rekomendasikan Service Mode

Studi kasus ini memiliki tiga kebutuhan Utama, yaitu data sangat rahasia dan diatur UU Perlindungan Data Pribadi, diakses ribuan instansi dengan pola akses yang tidak rata, dan membutuhkan skalabilitas tanpa menempatkan data di infrastruktur yang tidak dikendalikan penuh oleh negara. Karena itu pemetaan service model mengikuti tingkat sensitivitas komponen .Semakin sensitif data yang harus dijaga, semakin harus lebih banyak dikendalikan oleh negara. Kalau semakin tidak sensitif datanya, beban operasinya lebih sedikit juga alias tidak harus full dikendalikan oleh negara.

Jadi untuk rekomendasi service model dari kami adalah:
### 1. Iaas 
untuk database inti data kependudukan (NIK, alamat, biometrik) dan manajemen kunci enkripsi (HSM/KMS), ditempatkan di private cloud pemerintah : Untuk memenuhi kebutuhan kerahasiaan sesuai UU Perlindungan Data Pribadi, IaaS dipilih karena memberi kontrol penuh OS, database, dan enkripsi, sehingga tidak ada jalur akses pihak ketiga ke data sensitif dan kunci enkripsi dipegang oleh pemerintah. Pengguna tidak memiliki akses ke sistem, tetapi bisa minta ke pemerintah untuk memperbaiki, memperbarui, atau menghapus data(sesuai ketentuan hukum), mereka juga punya hak melihat Riwayat akses dan memberi atau membatalkan persetujuan. Sedangkan bank mengakses dengan persetujuan pengguna, dan polisi berdasarkan dasar hukum tanpa perlu persetujuan.

### 2. Paas 
untuk layanan verifikasi/API(termasuk verifikasi KYC), API gateway, dan portal pengecekan status publik: Untuk melayani ribuan instansi dengan pola akses yang tidak rata (lonjakan saat pemilu dan pendaftaran sekolah), PaaS dipilih karena bagian ini paling sering diakses dan jumlah penggunanya naik turun. Dengan PaaS, kapasitas bisa bertambah otomatis saat ramai tanpa pemerintah mengurus server dan sistem operasi satu per satu, sehingga tim bisa fokus pada aplikasinya. Saat akses sedang ramai yaitu API gateway, layanan verifikasi, dan portal cek status dapat diperluas ke public cloud yang berlokasi di Indonesia agar sistem tidak down. Hal ini aman karena bagian itu hanya menerima permintaan dan menampilkan jawaban singkat, seperti “true” atau “false”, tanpa menyimpan data sensitif. Data sensitif tetap tersimpan di private cloud pemerintah, dan public cloud hanya bertugas menambah kapasitas pelayanan waktu lagi ramai. Setiap permintaan tetap melewati autentikasi, pembatasan kuota, dan pencatatan akses. Dengan cara ini, kebutuhan skalabilitas terpenuhi tanpa data berada di infrastruktur yang tidak dikendalikan penuh oleh negara.

### 3. SaaS 
untuk email, helpdesk, dan kolaborasi internal: Untuk fungsi pendukung yang tidak berkaitan langsung dengan data kependudukan, SaaS dipilih karena fungsinya hanya pendukung dan dia tidak memproses data sensitif, sehingga cukup memakai layanan yang siap pakai tanpa mengurus server dan jaringan. Data pribadi pengguna (NIK, alamat, biometrik) dilarang dikirim lewat layanan ini.

Kesimpulan:
Pemetaan service model ini mengikuti tingkat sensitivitas komponen. IaaS dipakai untuk data inti (database dan kunci enkripsi) agar kendali penuh ada di pemerintah. PaaS dipakai untuk layanan akses (verifikasi/API (termasuk verifikasi KYC), API gateway, portal status) yang butuh kapasitas fleksibel saat ramai. SaaS dipakai untuk fungsi pendukung yg tidak sensitif seperti email dan helpdesk. Dengan begitu, data tetap rahasia sekaligus sistem tetap mampu melayani lonjakan akses.

## 3. Risiko dan Mitigasi

### 1. Risiko Serangan Denial-of-Service (DoS/DDoS)
- **Risiko** : Portal pengecekan status yang ditaruh di Public Cloud bisa jadi sasaran  serangan DoS atau DDoS. Penyerang bisa membanjiri server dengan request dalam jumlah besar, sehingga CPU, memori, dan bandwidth habis terpakai. Dampaknya, masyarakat maupun instansi jadi lambat mengakses layanan, bahkan sistem bisa sama sekali tidak bisa dibuka.
- **Mitigasi** : Menerapkan rate limiting untuk membatasi jumlah request yang masuk, gunakan firewall untuk menyaring lalu lintas jaringan, dan  IDS/IPS agar aktivitas mencurigakan bisa terdeteksi dan langsung diblokir. Selain itu, siapkan server cadangan supaya layanan tetap jalan kalau server utama sedang bermasalah.

### 2. Risiko Akses Tidak Sah dan Kebocoran Data
- **Risiko** : Celah keamanan dapat terjadi jika koneksi antara Public Cloud dan Private Cloud tidak diamankan dengan baik. Penyerang bisa memanfaatkan celah di API atau mencuri kredensial pengguna untuk masuk ke data kependudukan yang bersifat rahasia, seperti NIK, alamat, dan data biometrik.
- **Mitigasi** : Menerapkan Zero Trust Architecture, yaitu konsep di mana sistem tidak langsung percaya pada pengguna atau perangkat hanya karena berasal dari jaringan tertentu. Setiap permintaan akses wajib melewati proses autentikasi dan otorisasi. Selain itu, gunakan MFA (Multi-Factor Authentication), batasi hak akses dengan prinsip Least Privilege, dan pasang IDS untuk mendeteksi aktivitas yang mencurigakan.

### 3. Risiko Kesalahan Konfigurasi dan Pertukaran Data Antar-Cloud
- **Risiko** : Hybrid Cloud melibatkan komunikasi antara Private Cloud dan Public Cloud, jadi kalau ada salah konfigurasi jaringan atau aturan akses di firewall, lalu lintas yang seharusnya diblokir bisa lolos masuk ke Private Cloud. Selain itu, data di cache Public Cloud juga berpotensi tidak sinkron dengan data terbaru yang ada di Private Cloud.
- **Mitigasi** : Menerapkan firewall untuk mengatur lalu lintas jaringan, dan memastikan hanya komunikasi yang sudah diizinkan yang bisa lewat di antara kedua cloud. Terapkan juga prinsip Least Privilege supaya tiap layanan hanya punya akses sesuai kebutuhannya saja. Lakukan juga validasi dan pembaruan cache secara berkala agar informasi yang tampil tetap sesuai dengan data terbaru di Private Cloud.

## 4. Perbandingan dengan Alternatif yang Ditolak

Alternatif yang kami tolak adalah Public Cloud murni karena kurang sesuai dengan kebutuhan kerahasiaan Sistem Data Kependudukan. Public Cloud menggunakan infrastruktur penyedia layanan cloud komersial yang sumber dayanya digunakan bersama dengan pelanggan lain (multi-tenant). Hal ini membuat pemerintah tidak memiliki kendali penuh terhadap infrastruktur tempat data disimpan, sehingga berisiko terhadap keamanan data pribadi warga, terutama NIK dan biometrik.

Selain itu, penggunaan enkripsi saja belum cukup untuk mengatasi seluruh risiko karena pengelolaan infrastruktur dan akses fisik tetap melibatkan penyedia layanan cloud. Hal ini kurang sesuai dengan kebutuhan sistem yang mengharuskan data berada di infrastruktur yang dikendalikan penuh oleh negara.

Oleh karena itu, Hybrid Cloud lebih tepat dibandingkan Public Cloud murni karena data sensitif tetap disimpan di Private Cloud milik pemerintah, sedangkan Public Cloud dimanfaatkan untuk menangani komponen non-sensitif dan lonjakan akses. Dengan demikian, kebutuhan kerahasiaan data dan skalabilitas sistem dapat terpenuhi secara seimbang.