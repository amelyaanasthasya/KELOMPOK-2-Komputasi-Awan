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

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 4: Single Point of Failure — ditulis oleh [Firda Utami Sukman]

**Bukti di skenario:** "satu server yang menangani semua bagian sistem (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama"

**Kenapa ini keliru:** Terjadi single point of failure, karena seluruh fungsi utama FoodGo ditangani oleh satu server yang sama. Jadi, jika server mengalami overload atau crash, maka semua bagian sistem (pesanan, pembayaran, dan notifikasi kurir) bisa ikut berhenti. Hal ini berkaitan dengan masalah fault tolerance dalam sistem, yaitu kemampuan sistem untuk tetap berjalan ketika sebagian komponen mengalami kegagalan.

**Dampak ke FoodGo:** Saat ada promo besar atau jam makan siang, jumlah request akan meningkat dan server akan kewalahan memproses semuanya sendirian. Jika bagian pesanan mengalami bug, bagian pembayaran dan notifikasi kurir juga bisa ikut berhenti karena ssemuanya berada dalam proses monolitik (satu aplikasi/proses yang sama) di satu mesin. Akibatnya, seluruh layanan FoodGo dapat terganggu dan server harus di-restart secara manual.

**Solusi desain awal:** Memisahkan fungsi utama FoodGo menjadi beberapa service yang dapat berjalan secara terpisah, seperti Order Service, Payment Service, dan Notification Service. Kemudian, menggunakan beberapa server dan Load Balancer untuk membagi beban ke server yang tersedia. Dengan begitu, ketika salah satu server mengalami masalah, request dapat dialihkan ke server lain sehingga sistem tidak sepenuhnya bergantung pada satu server. Pembagian komputasi ke beberapa mesin juga membantu sistem menangani peningkatan trafik.

**Trade-off:** Kompleksitas sistem akan meningkat karena harus mengelola beberapa server dan layanan yang terpisah. Pemisahan layanan dapat menimbulkan masalah seperti sinkronisasi data agar informasi antar-layanan tetap menunjukkan status yang sesuai, sehingga membutuhkan manajemen infrastruktur yang lebih rumit.


## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]