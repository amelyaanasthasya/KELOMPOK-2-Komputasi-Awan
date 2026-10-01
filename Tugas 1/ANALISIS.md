# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [Kelompok 2]

| Nama | NIM | Kontribusi |
|---|---|---|
| Kadek Amelya Anasthasya Putri | 103072400073 | The Network is Reliable |
| Talitha Fairuzzahwa Nirwasita | 103072400035 | [pitfall/bagian yang dikerjakan] |
| Aisya Fadhilllah | 103072430004 | [pitfall/bagian yang dikerjakan] |
| Firda Utami Sukman | 103072400147 | Single Point of FailureSingle Point of Failure |

## Pitfall 1: The Network is Reliable — ditulis oleh Kadek Amelya Anasthasya Putri

**Bukti di skenario:** FoodGo memiliki asumsi dalam kode bahwa network is always reliable, no need for retry. Artinya, sistem menganggap jaringan selalu dapat diandalkan sehingga tidak menyiapkan mekanisme untuk menangani jika terjadi kegagalan komunikasi.

**Kenapa ini keliru:** Dalam sistem terdistribusi, komunikasi antar-service dilakukan melalui jaringan yang tidak selalu berjalan dengan baik. Koneksi bisa mengalami gangguan, request bisa gagal, atau service yang dituju tidak memberikan respons. Karena itu, sistem tidak bisa menganggap setiap komunikasi antar-service pasti berhasil.

**Dampak ke FoodGo:** Ketika Modul Pesanan berkomunikasi dengan Modul Pembayaran dan terjadi gangguan jaringan, request bisa gagal atau tidak mendapat respons. Karena tidak ada mekanisme retry, kegagalan tersebut tidak bisa ditangani dengan baik. Saat trafik sedang tinggi, masalah pada banyak request dapat membuat proses pesanan semakin terganggu, aplikasi menjadi lambat, dan resource server semakin terbebani hingga dapat menyebabkan server crash.

**Solusi desain awal:** Menerapkan retry dengan exponential backoff pada komunikasi antar-service. Jika request gagal, sistem dapat mencoba kembali beberapa kali dengan jeda yang semakin meningkat. Selain itu, circuit breaker dapat digunakan untuk menghentikan sementara request ke service yang sedang bermasalah agar gangguan tidak semakin meluas. Timeout juga dapat digunakan agar sistem tidak menunggu respons tanpa batas.

**Trade-off:** Retry dapat menambah jumlah request dan beban pada service yang sedang bermasalah. Jika dilakukan terlalu sering, retry justru dapat memperparah kondisi dan menyebabkan cascading failure. Karena itu, jumlah retry dan jeda antar percobaan perlu dibatasi.

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 4: Single Point of Failure — ditulis oleh Firda Utami Sukman

**Bukti di skenario:** "satu server yang menangani semua bagian sistem (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama"

**Kenapa ini keliru:** Terjadi single point of failure, karena seluruh fungsi utama FoodGo ditangani oleh satu server yang sama. Jadi, jika server mengalami overload atau crash, maka semua bagian sistem (pesanan, pembayaran, dan notifikasi kurir) bisa ikut berhenti. Hal ini berkaitan dengan masalah fault tolerance dalam sistem, yaitu kemampuan sistem untuk tetap berjalan ketika sebagian komponen mengalami kegagalan.

**Dampak ke FoodGo:** Saat ada promo besar atau jam makan siang, jumlah request akan meningkat dan server akan kewalahan memproses semuanya sendirian. Jika bagian pesanan mengalami bug, bagian pembayaran dan notifikasi kurir juga bisa ikut berhenti karena ssemuanya berada dalam proses monolitik (satu aplikasi/proses yang sama) di satu mesin. Akibatnya, seluruh layanan FoodGo dapat terganggu dan server harus di-restart secara manual.

**Solusi desain awal:** Memisahkan fungsi utama FoodGo menjadi beberapa service yang dapat berjalan secara terpisah, seperti Order Service, Payment Service, dan Notification Service. Kemudian, menggunakan beberapa server dan Load Balancer untuk membagi beban ke server yang tersedia. Dengan begitu, ketika salah satu server mengalami masalah, request dapat dialihkan ke server lain sehingga sistem tidak sepenuhnya bergantung pada satu server. Pembagian komputasi ke beberapa mesin juga membantu sistem menangani peningkatan trafik.

**Trade-off:** Kompleksitas sistem akan meningkat karena harus mengelola beberapa server dan layanan yang terpisah. Pemisahan layanan dapat menimbulkan masalah seperti sinkronisasi data agar informasi antar-layanan tetap menunjukkan status yang sesuai, sehingga membutuhkan manajemen infrastruktur yang lebih rumit.


## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]