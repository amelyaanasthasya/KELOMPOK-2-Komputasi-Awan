# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 2

| Nama | NIM | Kontribusi |
|---|---|---|
| Kadek Amelya Anasthasya Putri | 103072400073 | Pitfall 1 (The Network is Reliable) |
| Talitha Fairuzzahwa Nirwasita | 103072400035 | Pitfall 3 (bandwidth is infinite) |
| Aisya Fadhilllah | 103072430004 | Pitfall 2 (Latency is zero) |
| Firda Utami Sukman | 103072400147 | pitfall 4 (Single Point of Failure) |

## Pitfall 1: The Network is Reliable — ditulis oleh Kadek Amelya Anasthasya Putri

**Bukti di skenario:** FoodGo memiliki asumsi dalam kode bahwa network is always reliable, no need for retry. Artinya, sistem menganggap jaringan selalu dapat diandalkan sehingga tidak menyiapkan mekanisme untuk menangani jika terjadi kegagalan komunikasi.

**Kenapa ini keliru:** Dalam sistem terdistribusi, komunikasi antar-service dilakukan melalui jaringan yang tidak selalu berjalan dengan baik. Koneksi bisa mengalami gangguan, request bisa gagal, atau service yang dituju tidak memberikan respons. Karena itu, sistem tidak bisa menganggap setiap komunikasi antar-service pasti berhasil.

**Dampak ke FoodGo:** Ketika Modul Pesanan berkomunikasi dengan Modul Pembayaran dan terjadi gangguan jaringan, request bisa gagal atau tidak mendapat respons. Karena tidak ada mekanisme retry, kegagalan tersebut tidak bisa ditangani dengan baik. Saat trafik sedang tinggi, masalah pada banyak request dapat membuat proses pesanan semakin terganggu, aplikasi menjadi lambat, dan resource server semakin terbebani hingga dapat menyebabkan server crash.

**Solusi desain awal:** Menerapkan retry dengan exponential backoff pada komunikasi antar-service. Jika request gagal, sistem dapat mencoba kembali beberapa kali dengan jeda yang semakin meningkat. Selain itu, circuit breaker dapat digunakan untuk menghentikan sementara request ke service yang sedang bermasalah agar gangguan tidak semakin meluas. Timeout juga dapat digunakan agar sistem tidak menunggu respons tanpa batas.

**Trade-off:** Retry dapat menambah jumlah request dan beban pada service yang sedang bermasalah. Jika dilakukan terlalu sering, retry justru dapat memperparah kondisi dan menyebabkan cascading failure. Karena itu, jumlah retry dan jeda antar percobaan perlu dibatasi.

---

## Pitfall 2: latency is zero — ditulis oleh Aisya Fadhilllah

**Bukti di skenario:** Tim menemukan didalam kodenya "Tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).", "Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama."

**Kenapa ini keliru:** Karena di sistem FoodGo tim mengira kirim data lewat internet itu kecepatannya instan 0 detik seperti baca data di laptop sendiri. Karena mengira tidak akan pernah ada jeda/macet, mereka membuat modul pesanan menunggu modul pembayaran sampai dapat jawaban tanpa batas waktu, dan menumpuk semua fitur dalam satu server yang sama.

**Dampak ke FoodGo:** Saat pembeli lagi ramai, jalur pembayaran mulai melambat. Karena tidak ada batas waktu tunggu (timeout), modul pesanan ikut crash karena terus-terusan menunggu tanpa kejelasan hingga antrian pembeli di belakangnya makin panjang. Karena semua fitur (pesanan, pembayaran, notifikasi) tinggal di satu proses yang sama yang dijalankan di satu server yang sama, kemacetan di bagian pembayaran bikin seluruh server kehabisan memori, crash, dan harus dimatikan lalu dinyalakan ulang secara manual (restart).

**Solusi desain awal:** Untuk mengatasi masalah tersebut, tim perlu membatasi waktu tunggu panggilan antar-proses (misal 2–3 detik) agar saat proses pembayaran melambat, proses pesanan dapat segera memutus koneksi dan melepas thread CPU sehingga server tidak kehabisan memori atau mengalami crash. Selain itu, eksekusi tugas seperti pencarian driver atau pengiriman notifikasi sebaiknya dialihkan ke proses worker latar belakang melalui antrian agar proses pesanan dapat langsung menyelesaikan tugas utamanya dan siap melayani request berikutnya di server. Terakhir, melakukan pemisahan eksekusi modul-modul aplikasi ke dalam proses terpisah atau di server yang terpisah (decoupling), sehingga jika proses pembayaran mengalami kemacetan, proses pesanan dan navigasi katalog di server lain tetap dapat berjalan dengan normal.

**Trade-off:** 
1. Kompleksitas Kode pada Proses Aplikasi
 Developer harus menulis logika tambahan di dalam proses aplikasi untuk mengelola kondisi saat panggilan membalas timeout (misalnya pembuatan fitur tombol coba lagi atau pembatalan transaksi secara otomatis).
2. Konsistensi Data Tertunda
 Karena proses tidak lagi menunggu semua eksekusi selesai secara instan di dalam server, status data tidak langsung berubah menjadi "Selesai" di detik yang sama, melainkan pengguna akan melihat status perantara seperti "Pesanan Sedang Diproses".

---

## Pitfall 3: bandwidth is infinite — ditulis oleh Talitha Fairuzzahwa Nirwasita

**Bukti di skenario:** FoodGo mengalami lonjakan jumlah pesanan saat jam makan siang atau promo besar. Pada kondisi tersebut, aplikasi menjadi sangat lambat, beberapa permintaan mengalami timeout, dan satu server yang menangani modul pesanan, pembayaran, serta notifikasi kurir menjadi kewalahan.

**Kenapa ini keliru:** Asumsi bahwa bandwidth jaringan tidak terbatas merupakan hal yang keliru karena kapasitas jaringan dalam mengirimkan data memiliki batas. Ketika jumlah permintaan meningkat, volume data yang dikirim dan diterima juga bertambah sehingga dapat menyebabkan kepadatan jaringan (network congestion). Dalam sistem terdistribusi, komunikasi antarservice membutuhkan bandwidth yang memadai agar pertukaran data dapat berjalan dengan lancar.

**Dampak ke FoodGo:** Ketika terjadi lonjakan pesanan, banyak permintaan harus diproses dan data perlu dipertukarkan antara modul pesanan, pembayaran, dan notifikasi kurir. Peningkatan lalu lintas data dapat menyebabkan antrean komunikasi dan memperlambat respons antar modul. Akibatnya, waktu pemrosesan pesanan meningkat, beberapa permintaan megagame timeout, dan beban server semakin tinggi hingga berpotensi menyebabkan crash.

**Solusi desain awal:** Menerapkan mekanisme pembatasan permintaan (rate limiting) untuk mengendalikan jumlah request yang masuk, serta menggunakan message queue untuk mengatur komunikasi antar modul agar tidak semua permintaan harus diproses secara bersamaan. Selain itu, melakukan pemantauan penggunaan bandwidth dan mengoptimalkan ukuran data yang dikirim antarservice.

**Trade-off:** 
1. Rate Limiting
Pembatasan permintaan digunakan untuk membatasi jumlah permintaan yang diproses dalam waktu tertentu, solusi ini memiliki konsekuensi yaitu sebagian request harus menunggu atau ditolak sementara.
2. Message Queue
Solusi ini berfungsi untuk mengatur waktu tunggu (urutan) pemoresesan permintaan yang berfungsi agar tidak semua request menumpuk dan di proses bersamaan. Konsekuensi dari solusi ini adalah pengguna mungkin perlu menunggu sedikit lebih lama sampai notifikasi atau proses tertentu selesai.
---

## Pitfall 4: Single Point of Failure — ditulis oleh Firda Utami Sukman

**Bukti di skenario:** "satu server yang menangani semua bagian sistem (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama"

**Kenapa ini keliru:** Terjadi single point of failure, karena seluruh fungsi utama FoodGo ditangani oleh satu server yang sama. Jadi, jika server mengalami overload atau crash, maka semua bagian sistem (pesanan, pembayaran, dan notifikasi kurir) bisa ikut berhenti. Hal ini berkaitan dengan masalah fault tolerance dalam sistem, yaitu kemampuan sistem untuk tetap berjalan ketika sebagian komponen mengalami kegagalan.

**Dampak ke FoodGo:** Saat ada promo besar atau jam makan siang, jumlah request akan meningkat dan server akan kewalahan memproses semuanya sendirian. Jika bagian pesanan mengalami bug, bagian pembayaran dan notifikasi kurir juga bisa ikut berhenti karena ssemuanya berada dalam proses monolitik (satu aplikasi/proses yang sama) di satu mesin. Akibatnya, seluruh layanan FoodGo dapat terganggu dan server harus di-restart secara manual.

**Solusi desain awal:** Memisahkan fungsi utama FoodGo menjadi beberapa service yang dapat berjalan secara terpisah, seperti Order Service, Payment Service, dan Notification Service. Kemudian, menggunakan beberapa server dan Load Balancer untuk membagi beban ke server yang tersedia. Dengan begitu, ketika salah satu server mengalami masalah, request dapat dialihkan ke server lain sehingga sistem tidak sepenuhnya bergantung pada satu server. Pembagian komputasi ke beberapa mesin juga membantu sistem menangani peningkatan trafik.

**Trade-off:** Kompleksitas sistem akan meningkat karena harus mengelola beberapa server dan layanan yang terpisah. Pemisahan layanan dapat menimbulkan masalah seperti sinkronisasi data agar informasi antar-layanan tetap menunjukkan status yang sesuai, sehingga membutuhkan manajemen infrastruktur yang lebih rumit.

---

## Kesimpulan Kelompok

Jika FoodGo memperbaiki ketiga pitfall tersebut, arsitektur yang disarankan adalah memisahkan sistem monolitik menjadi beberapa service, seperti Order Service, Payment Service, dan Notification Service, yang dapat berjalan secara terpisah dan menggunakan beberapa server dengan Load Balancer untuk membagi beban. Komunikasi antar-service perlu menggunakan timeout agar suatu service tidak menunggu respons tanpa batas, serta retry dengan jeda ketika terjadi kegagalan komunikasi. Untuk proses yang tidak harus dilakukan secara langsung, seperti notifikasi kurir, dapat menggunakan Message Queue agar pekerjaan dapat diproses secara bertahap. Dengan rancangan ini, kegagalan atau beban tinggi pada satu bagian tidak langsung menyebabkan seluruh sistem berhenti, meskipun konsekuensinya adalah arsitektur menjadi lebih kompleks dan membutuhkan pengelolaan komunikasi serta konsistensi data antar-service.