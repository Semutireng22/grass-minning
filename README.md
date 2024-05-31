# GRASS Script

Script Python untuk menjalankan mining grass secara otomatis menggunakan WebSocket proxy.

## Instalasi

1. Pastikan Anda memiliki Python yang terinstal di sistem Ubuntu VPS Anda. Jika belum, Anda dapat mengunduhnya dengan perintah berikut:
    ```bash
    sudo apt update
    sudo apt install python3
    ```

2. Klon repository ini ke VPS Anda:
    ```bash
    git clone https://github.com/Semutireng22/grass-minning.git
    cd grass-minning
    ```

3. Instal modul yang diperlukan menggunakan pip:
    ```bash
    pip install -r requirements.txt
    ```

4. Anda perlu menginstal `screen` agar dapat menjalankan skrip di latar belakang. Jika belum terinstal, lakukan instalasi dengan perintah:
    ```bash
    sudo apt install screen
    ```

## Penggunaan

1. Pastikan Anda sudah login ke Grass melalui browser Anda sebelum menjalankan skrip.

2. Jalankan skrip utama dengan menjalankan perintah:
    ```bash
    python main.py
    ```

3. Ikuti instruksi yang muncul di terminal untuk memilih URL proxy dan memasukkan User ID Anda.

4. Bot akan mulai menjalankan mining grass secara otomatis menggunakan proxy yang dipilih.

## Menjalankan Skrip di Latar Belakang Menggunakan Screen

Jika Anda ingin menjalankan skrip di latar belakang sehingga dapat keluar dari terminal tanpa memengaruhi proses skrip, Anda dapat menggunakan `screen`.

1. Buat sesi `screen` baru dengan nama sesi tertentu:
    ```bash
    screen -S grass
    ```

2. Jalankan skrip di dalam sesi `screen` yang baru saja dibuat:
    ```bash
    python main.py
    ```

3. Tekan `Ctrl + A`, lalu tekan `D` untuk mengembalikan ke prompt terminal utama. Skrip akan tetap berjalan di latar belakang.

4. Untuk kembali ke sesi `screen` dan melihat output skrip, jalankan perintah berikut:
    ```bash
    screen -rd grass
    ```

## Mengambil UID Grass

### Pengguna PC (Chrome)

1. Pastikan Anda sudah login ke Grass melalui browser Chrome Anda.
2. Buka konsol Chrome dengan menekan `Ctrl + Shift + J` atau `Cmd + Option + J` di macOS.
3. Tempelkan kode berikut di konsol Chrome dan tekan Enter:
    ```javascript
    console.log(localStorage.getItem('userId'));
    ```
4. Anda akan melihat UID Grass di konsol Chrome.

### Pengguna Seluler

1. Pastikan Anda sudah login ke Grass melalui browser di perangkat seluler Anda.
2. Buka pengembang browser dengan mengetuk ikon menu (biasanya tiga titik atau garis) dan pilih opsi "Developer tools" atau "Developer mode".
3. Pilih opsi "Console" atau "Javascript Console".
4. Tempelkan kode berikut di konsol dan tekan Enter:
    ```javascript
    console.log(localStorage.getItem('userId'));
    ```
5. Anda akan melihat UID Grass di konsol browser seluler.

## Bergabung dengan Channel Kami

Bergabunglah dengan channel kami di [UGD Airdrop](https://t.me/UGDAirdrop) untuk mendapatkan informasi terbaru seputar airdrop dan promo-promo menarik lainnya!

## Kontribusi

Anda dapat berkontribusi pada pengembangan skrip ini dengan mengirimkan _pull request_ atau melaporkan _issue_ di [repository GitHub](https://github.com/Semutireng22/grass-minning).