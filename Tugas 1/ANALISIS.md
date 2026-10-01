# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [Kelompok 2]

| Nama | NIM | Kontribusi |
|---|---|---|
| Kadek Amelya Anasthasya Putri | 103072400073 | [pitfall/bagian yang dikerjakan] |
| Talitha Fairuzzahwa Nirwasita | 103072400035 | [pitfall/bagian yang dikerjakan] |
| Aisya Fadhilllah | 103072430004 | [pitfall/bagian yang dikerjakan] |
| Firda Utami Sukman | 103072400147 | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: bandwidth is infinite — ditulis oleh [Talitha Fairuzzahwa Nirwasita]

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

## Pitfall 4: Single Point of Failure — ditulis oleh [Firda Utami Sukman]

**Bukti di skenario:** "satu server yang menangani semua bagian sistem (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama"

**Kenapa ini keliru:** Terjadi single point of failure, karena seluruh fungsi utama FoodGo ditangani oleh satu server yang sama. Jadi, jika server mengalami overload atau crash, maka semua bagian sistem (pesanan, pembayaran, dan notifikasi kurir) bisa ikut berhenti. Hal ini berkaitan dengan masalah fault tolerance dalam sistem, yaitu kemampuan sistem untuk tetap berjalan ketika sebagian komponen mengalami kegagalan.

**Dampak ke FoodGo:** Saat ada promo besar atau jam makan siang, jumlah request akan meningkat dan server akan kewalahan memproses semuanya sendirian. Jika bagian pesanan mengalami bug, bagian pembayaran dan notifikasi kurir juga bisa ikut berhenti karena ssemuanya berada dalam proses monolitik (satu aplikasi/proses yang sama) di satu mesin. Akibatnya, seluruh layanan FoodGo dapat terganggu dan server harus di-restart secara manual.

**Solusi desain awal:** Memisahkan fungsi utama FoodGo menjadi beberapa service yang dapat berjalan secara terpisah, seperti Order Service, Payment Service, dan Notification Service. Kemudian, menggunakan beberapa server dan Load Balancer untuk membagi beban ke server yang tersedia. Dengan begitu, ketika salah satu server mengalami masalah, request dapat dialihkan ke server lain sehingga sistem tidak sepenuhnya bergantung pada satu server. Pembagian komputasi ke beberapa mesin juga membantu sistem menangani peningkatan trafik.

**Trade-off:** Kompleksitas sistem akan meningkat karena harus mengelola beberapa server dan layanan yang terpisah. Pemisahan layanan dapat menimbulkan masalah seperti sinkronisasi data agar informasi antar-layanan tetap menunjukkan status yang sesuai, sehingga membutuhkan manajemen infrastruktur yang lebih rumit.

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]