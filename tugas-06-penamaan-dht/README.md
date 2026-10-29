# ANALISIS

## Analisis Pemilihan DHT/Chord
Pada sistem FoodGo, ID kurir perlu dipetakan ke alamat IP yang dapat berubah sewaktu-waktu. Oleh karena itu, digunakan **Distributed Hash Table (DHT)** dengan pendekatan **Chord** untuk menentukan node yang bertanggung jawab terhadap setiap ID kurir.

Dibandingkan tabel pemetaan terpusat, DHT mendistribusikan tanggung jawab penyimpanan ke beberapa node sehingga tidak bergantung pada satu server pusat. Jika satu node keluar, tanggung jawabnya dapat dialihkan ke node lain sesuai aturan successor.

Dibandingkan DNS konvensional, Chord menyediakan mekanisme penentuan node berdasarkan hash ID dalam ring terdistribusi. Hal ini sesuai untuk simulasi FoodGo yang membutuhkan pemetaan ID kurir ke alamat IP secara dinamis.

Pada implementasi ini, ID kurir dan ID node di-hash ke ruang identifier 0–255 menggunakan SHA-1 yang hasilnya dibatasi dengan modulo 256. Node dengan ID terkecil yang lebih besar atau sama dengan hash kurir menjadi successor yang bertanggung jawab. Jika tidak ada node yang memenuhi kondisi tersebut, pencarian kembali ke node dengan ID terkecil.

Simulasi ini masih berjalan dalam satu proses Python, sehingga distribusi node dan perpindahan tanggung jawab merupakan simulasi, bukan komunikasi jaringan terdistribusi sungguhan.

## Topologi dan Pemetaan Chord DHT sekaligus penjelasan dari analisis soal nomor 3
Pada kode kami menggunakan konsisten hashing (m=8, ruang identifier 0-255) dengan rumus `SHA-1 % 256`. Aturan dasar Chord adalah setiap data kurir akan disimpan di node `successor (node aktif dengan nilai id hash terkecil yang lebih besar samadengan (>=) hash kurir (node id hash yang terbesar pertama setelah hash kurir)) dan jika tidak ada id node yang lebih besar dari id kurir, maka dia akan wrap-around alias putar balik ke node awal`. Jika ada suatu node yang keluar dari ring, data yang ada pada node tersebut akan digantikan atau diambil alih oleh node successor terdekat berikutnya(node aktif pertama yang id hashnya lebih besar samadengan hash data tersebut). Jika node yang keluar tidak memegang data apapun, dia akan keluar tanpa berpengaruh apapun pada mappingnya. Di output program kita node yang keluar yaitu node-jakarta-1(177) tidak memegang data kurir apapun sehingga dia keluar tanpa menyerahkan datanya ke node lain, dan tidak berpengaruh apapun terhadap pemetaan data ataupun urutan ring.

### Topologi Sebelum Perubahan 
Nilai hash dan alamat node ring sebelum perubahan:
- node-jakarta-1 (id = 177), alamat 10.0.0.1
- node-jakarta-2 (id = 102), alamat 10.0.0.2
- node-bandung-1 (id = 40), alamat 10.0.0.3
- node-ssurabaya-1 (id = 136), alamat 10.0.0.4

Pengurutan nilai hash node untuk memetakkan letak kurir:
- node-bandung-1 (id = 40)
- node-jakarta-2 (id = 102)
- node-surabaya-1 (id = 136)
- node-jakarta-1 (id = 177)

### Pemetaan Kurir ke Node Successor (Walkthrough)
Setelah semua node diurutkan, kurir juga akan di urutkan dari hash terkecil ke terbesar untuk dipetakkan sesuai node succesor (node aktif id hash terkecil >= hash kurir (node id hash yang terbesar pertama setelah hash kurir)).

Pengurutan kurir dari hash terkecil dan pemetaan kurir:
- kurir-001 (28) dia akan disimpan ke successor (40) karena `40 adalah node yg lebih besar pertama dari 28`
- kurir-002 (50) dia akan disimpan ke successor (102) karena `102 adalah node yg lebih besar pertama dari 50`
- kurir-test-13 (111) dia akan disimpan ke successor (136) karena `136 adalah node yg lebih besar pertama dari 111`
- kurir-003 (132) dia juga akan disimpan ke successor (136) karena `136 adalah node yg lebih besar pertama dari 132`

### Analisis Perubahan Topologi
Ada node yang baru bergabung di dalam ring (node-medan-1) dengan (id hash = 123), jadi posisinya ditaruh `diantara node-jakarta-2(102) dan node-surabaya-1(136)`. Setelah itu kurir yang punya id <= node pertama akan dipetakkan ulang, `kurir-test-13` dengan (hash=111) yang kondisinya `111 <= 123` (node lebih besar pertama yg dijumpai oleh kurir-test-13) yang sebelumnya bertanggungjawab di node-surabaya-1 (136) berpindah ke node-medan-1 (123). Namun `kurir-003 (132)` tetap berada di node-surabaya-1 (136) karena kondisi dia tetap `132 <= 136`.

Ada node yang keluar dari ring, yaitu node-jakarta-1 (177). Node ini tidak menyimpan kurir manapun sehingga tidak berpengaruh ke perubahan pemetaan kurir dan node ini bisa langsung keluar tanpa mengubah hasil yang ada

Urutan Node dan Kurir yang bertanggungjawab setelah perubahan Topologi:
- node-bandung-1 (id = 40), kurir-001 (28)
- node-jakarta-2 (id = 102), kurir-002 (50)
- node-medan-1 (id = 123), kurir-test-13 (111) 
- node-surabaya-1 (id = 136), kurir-003 (132)

# DIAGRAM RING
Diagram Ring terdapat pada file "bukti"