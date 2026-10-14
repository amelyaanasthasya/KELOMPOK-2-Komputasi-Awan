## Analisis

### 1. Mengapa FoodGo Membutuhkan Leader?

FoodGo membutuhkan leader untuk mengatur antrean pesanan agar semua server memiliki acuan yang sama dalam memproses pesanan. Tanpa leader, beberapa server dapat menentukan urutan pesanan yang berbeda karena jam yang tidak sinkron. Hal ini berpotensi menyebabkan konflik urutan atau pemrosesan pesanan yang sama lebih dari satu kali. Dengan adanya leader, koordinasi pemrosesan pesanan dapat dilakukan secara terpusat sehingga konflik dapat dikurangi.

### 2. Mengapa Menggunakan Bully Algorithm dibandingkan Raft?

Bully Algorithm dipilih karena konsepnya lebih sederhana untuk disimulasikan pada lima node. Setiap node memiliki ID, dan node dengan ID tertinggi yang masih aktif akan menjadi leader. Ketika leader mati, node lain dapat memulai election untuk memilih leader pengganti.

Sementara itu, Raft menggunakan mekanisme konsensus yang lebih lengkap, seperti pemilihan leader, replikasi log, dan pengelolaan komitmen data. Raft lebih sesuai untuk sistem terdistribusi yang membutuhkan konsistensi data dengan mekanisme yang lebih kuat, tetapi implementasinya lebih kompleks. Untuk tugas ini, Bully Algorithm lebih mudah digunakan untuk mempelajari proses pemilihan dan pergantian leader.

Namun, Bully Algorithm saja belum menjamin urutan pesanan konsisten atau mencegah pemrosesan ganda. FoodGo tetap memerlukan mekanisme tambahan untuk mengatur antrean, menyinkronkan data, dan memastikan setiap pesanan diproses dengan benar.

### 3. Hasil Pengujian

**Skenario 1 — Start normal**

Kelima node dijalankan sebagai lima proses Python terpisah dengan port TCP yang berbeda. Hasil pengujian menunjukkan Node 5 terpilih menjadi leader karena memiliki ID tertinggi. Node lain menerima pesan `COORDINATOR` dan mencatat Node 5 sebagai leader.

**Skenario 2 — Leader mati**

Setelah proses Node 5 dihentikan menggunakan `Ctrl+C`, node lain mendeteksi bahwa leader tidak dapat dihubungi dan memulai pemilihan ulang. Hasil pengujian menunjukkan Node 4 terpilih menjadi leader baru karena merupakan node aktif dengan ID tertinggi setelah Node 5 mati.

Berdasarkan kedua skenario, implementasi Bully Algorithm berhasil menunjukkan proses pemilihan leader awal dan pemilihan ulang ketika leader berhenti berjalan. Pengujian ini juga menunjukkan bahwa sistem dapat memilih pemimpin pengganti, meskipun konsistensi urutan pesanan tetap memerlukan mekanisme tambahan.