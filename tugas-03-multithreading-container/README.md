## Analisis

### 1. Race Condition

*Race condition* adalah kondisi ketika beberapa thread mengakses dan mengubah data yang sama secara bersamaan sehingga hasil akhirnya berpotensi tidak sesuai harapan. Pada program simulasi FoodGo, variabel `processed_count` digunakan untuk menghitung jumlah pesanan yang berhasil diproses oleh seluruh thread.

Tanpa penguncian, beberapa thread dapat menjalankan operasi penambahan counter secara bersamaan. Hal ini berpotensi menyebabkan pembaruan nilai saling tertimpa sehingga jumlah pesanan yang tercatat kurang dari jumlah sebenarnya. Dalam percobaan ini, hasil tanpa kunci tetap mencapai 100. Namun, hal tersebut tidak menjamin bahwa *race condition* tidak dapat terjadi.

### 2. Perbaikan dengan Lock

Untuk mencegah *race condition*, program menggunakan `threading.Lock()`. Lock membatasi akses ke bagian kode yang mengubah nilai `processed_count`, sehingga hanya satu thread yang dapat melakukan penambahan counter pada satu waktu.

Penguncian dilakukan menggunakan `with lock:` sebelum menjalankan `processed_count += 1`. Dengan demikian, proses pembaruan counter menjadi lebih aman dan hasil perhitungan tetap sesuai dengan jumlah pesanan yang diproses. Setelah menggunakan Lock, program menghasilkan 100 pesanan dari total 100 pesanan.

### 3. Alasan Menggunakan Threading

Program menggunakan *threading* karena simulasi pemrosesan pesanan melibatkan operasi yang menunggu, yaitu `time.sleep()`. Threading memungkinkan beberapa pekerjaan berjalan secara bersamaan sehingga waktu tunggu satu thread dapat dimanfaatkan oleh thread lainnya.

Dibandingkan *multiprocessing*, threading lebih sederhana untuk simulasi ini karena beberapa thread dapat berbagi variabel `processed_count` dalam satu proses. Sebaliknya, multiprocessing menggunakan proses terpisah dengan ruang memori masing-masing sehingga membutuhkan mekanisme komunikasi atau berbagi data tambahan untuk mengumpulkan counter.

Threading juga berbeda dari proses OS secara keseluruhan: thread tetap dijadwalkan oleh sistem operasi, tetapi beberapa thread dalam program ini berada di dalam satu proses yang sama. Karena tugas ini berfokus pada simulasi pemrosesan pesanan dengan operasi menunggu, threading sudah memadai dan lebih sederhana untuk digunakan.