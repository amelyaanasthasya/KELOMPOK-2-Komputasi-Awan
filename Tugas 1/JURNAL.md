# Jurnal Proses — Tugas 1

## 1 Oktober 2026
- Peserta: 
1. Kadek Amelya Anasthasya Putri(103072400073) 
2. Talitha Fairuzzahwa Nirwasita (103072400035) 
3. Aisya Fadhilllah (103072430004) 
4. Firda Utami Sukman (103072400147)

- Poin diskusi: ...
- Perbedaan pendapat (jika ada): ...

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 1 Oktober 2026 | ChatGPT | Menanyakan konsep Single Point of Failure (SPOF) pada kasus FoodGo | Dijelaskan bahwa SPOF adalah satu komponen yang jika mengalami masalah dapat membuat sistem lain ikut terganggu. Pada FoodGo, satu server yang menangani semua bagian sistem menjadi titik kegagalan karena jika server tersebut crash, beberapa layanan juga ikut berhenti. | Penjelasan tersebut digunakan untuk memahami konsep SPOF, kemudian diterapkan pada kasus FoodGo dan ditulis kembali dengan pemahaman sendiri. |
| 1 Oktober 2026 | ChatGPT | Bantu brainstroming dari kasus FoodGo tersebut dan analisis pitfall The Bandwidth is Infinite, dan gambaran beberapa prediksi solusi | Dalam kasus FoodGo, masalah muncul ketika trafik atau pesanan melonjak sehingga semakin banyak request dan data yang harus dikirim serta diproses. Hal ini dapat menunjukkan bahwa sistem belum memperhitungkan keterbatasan kapasitas komunikasi jaringan. Kondisi tersebut berkaitan dengan pitfall The Bandwidth is Infinite, yaitu asumsi bahwa jaringan mampu menangani data dalam jumlah berapa pun tanpa masalah. Jika komunikasi menjadi terlalu padat, respons dapat melambat dan berpotensi menyebabkan timeout. Beberapa solusi yang bisa dipertimbangkan adalah mengurangi data yang dikirim, menerapkan rate limiting, menggunakan message queue, load balancing, atau memisahkan service agar beban tidak terlalu terpusat. | Analisis Kasus -> ditemukan masalah utama yaitu sistem belum dirancang untuk menghadapi komunikasi/data dalam jumlah besar. Analisis Pitfall -> asumsi bahwa bandwidth jaringan tidak terbatas itu salah karena ada hubungan antara banyaknya request masuk pasti berpengaruh pada kepadatan jaringan. Analisis Solusi -> dari solusi yang diberikan, solusi yang diambil rate limiting dan Message queue |
| 1 Oktober 2026 | ChatGPT | Apa maksud pitfall “The Network is Reliable” pada studi kasus FoodGo dan apa saja poin yang perlu dianalisis? | AI menjelaskan bahwa asumsi jaringan selalu reliable merupakan kesalahan dalam sistem terdistribusi karena komunikasi antar-service dapat mengalami kegagalan. AI juga menyarankan untuk menghubungkan pitfall dengan bukti di skenario, dampak, solusi, dan trade-off. | Saya memahami kembali konsep tersebut dan memilih sendiri bagian yang relevan dengan skenario FoodGo. Penjelasan kemudian saya susun ulang menggunakan pemahaman dan bahasa saya sendiri. |