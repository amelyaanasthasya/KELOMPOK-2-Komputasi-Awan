# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
## Percobaan 1
- Hasil `processed_count` yang didapat: 0 (seharusnya 100)
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Kareena bagian pembagian tugas dan pembuat thread pada TODO 3 belum diimplementasikan jadi belum ada thread yang memproses pesanan dan menambah nilai counter (race condition).

## Percobaan 2
- Hasil `processed_count` setelah perbaikan: 100, Counter ini menghasilkan nilai yang benar. Namus tanpa sinkronisasi, thread masih bisa mengakses atau mengubah counter secara bersamaan. Percobaan ini belum membuktikan program bebas dari race condition.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100, Penggunaan threading.Lock() melindungi proses penambahan counter sehingga hanya 1 thread yang dapat menjalankan bgian code dalam 1 waktu.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: 

Kendala: Docker Desktop sempat mengalami loading terus-menerus dan proses build gagal karena file requirements.txt tidak ditemukan.

Solusi: Memastikan Docker Desktop berjalan, membuat file requirements.txt di folder proyek, lalu menjalankan ulang proses build.

Hasil: Docker image foodgo-order-sim berhasil dibuat dan container berhasil dijalankan dengan hasil Total pesanan diproses: 100 (seharusnya 100)

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 14 Oktober 2026 | ChatGPT | Gambaran besar tugas 3 | Gambaran besar Tugas : 1. Pahami skeleton program -> Buka src/order_simulator.py dan identifikasi bagian # TODO yang harus kamu isi. 2. Uji race condition -> Jalankan simulasi tanpa Lock, amati apakah counter pesanan menghasilkan angka yang salah, lalu simpan bukti hasilnya. 3. Perbaiki dengan threading.Lock() -> Jalankan ulang dan bandingkan counter sebelum dan sesudah sinkronisasi. 4. Jalankan dengan Docker -> Lengkapi Dockerfile sendiri, build image, jalankan container, lalu simpan bukti keberhasilannya. 5. Dokumentasikan hasil -> Isi README.md untuk analisis dan JURNAL.md untuk log percobaan, perbandingan hasil, kendala Docker, serta penggunaan AI. | Menelusuri skeleton program dan mengerjakan bedasarkan perintah TODO. Membuat keseluruhan algoritma dan menganalisis perbedaan hasil output |
| 14 Oktober 2026 | ChatGPT | Pemahaman konsep yang diuji serta gambaran kodenya. | AI menjelaskan konsep multithreading, race condition, penggunaan Lock, dan Docker, beserta contoh kode Python untuk simulasi pesanan. | Penjelasan digunakan untuk memahami konsep tugas, kemudian disesuaikan dengan skeleton program dari dosen dan hasil pengujian yang dilakukan sendiri. |