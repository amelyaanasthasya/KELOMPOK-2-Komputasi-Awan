# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Memahami alur pertukaran pesan ELECTION, OK, dan COORDINATOR serta memastikan node dengan ID tertinggi menjadi leader.
- Solusi: Penanganan pesan, mekanisme pemilihan leader, broadcast COORDINATOR, dan pemantauan koneksi leader.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi: Kelima node dijalankan sebagai proses Python terpisah pada port TCP yang berbeda. Node 5 terpilih menjadi leader karena memiliki ID tertinggi. Node lain menerima pesan COORDINATOR dan mencatat Node 5 sebagai leader.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4
- Berapa lama waktu sampai leader baru terdeteksi: Sekitar beberapa detik setelah Node 5 dimatikan. Setelah proses Node 5 dihentikan menggunakan Ctrl+C, node lain mendeteksi kegagalan koneksi dan memulai election. Node 4 kemudian terpilih sebagai leader baru dan mengumumkannya kepada node lain.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 14 Oktober 2026 | ChatGPT | Jelaskan gambaran besar dan alur pengerjaan Tugas 5 | Tugas 5 (Pekan 5) membahas Koordinasi dan Konsensus dalam sistem terdistribusi, khususnya penggunaan Bully Algorithm untuk memilih pemimpin (leader) di antara beberapa node. Pada tugas ini, mahasiswa diminta membuat simulasi lima node virtual yang berjalan sebagai lima proses Python terpisah di satu laptop. Setiap node menggunakan port TCP yang berbeda dan berkomunikasi melalui localhost. Pengerjaan dimulai dengan melengkapi bagian TODO pada file src/node.py, yang mencakup penanganan pesan ELECTION, OK, dan COORDINATOR, proses pemilihan leader, pengumuman leader terpilih, serta pemantauan kondisi leader. Setelah implementasi selesai, program diperiksa untuk memastikan tidak ada kesalahan sintaks, kemudian dijalankan melalui lima terminal berbeda dengan perintah Python sesuai ID, port, dan daftar peer masing-masing node. Pengujian dilakukan melalui dua skenario. Pertama, kelima node dijalankan untuk mengamati pemilihan leader awal, yang seharusnya menghasilkan Node 5 sebagai leader karena memiliki ID tertinggi. Kedua, proses Node 5 dihentikan menggunakan Ctrl + C untuk menguji kemampuan node lain dalam mendeteksi kegagalan dan melakukan pemilihan ulang, dengan hasil yang diharapkan berupa Node 4 sebagai leader baru.
Hasil pengujian kemudian didokumentasikan melalui screenshot atau log terminal dan disimpan di folder bukti/. Selain itu, README.md diisi dengan analisis mengenai pentingnya leader bagi koordinasi antrean pesanan FoodGo, alasan penggunaan Bully Algorithm dibandingkan Raft, serta hasil kedua skenario. Sementara itu, JURNAL.md digunakan untuk mencatat kendala, solusi, dan hasil pengerjaan tugas. | Breakdown dan memperbaiki kode node.py lalu dirunning satu satu dan mematikan terminal kelima dengan ctrl+c. Kemudian dianalisis |