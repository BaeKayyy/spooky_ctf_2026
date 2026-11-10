# Philophobia --- Sonnet 18 dan XOR Key

**Author:** Abhishek Kr Gupta\
**Event:** SpookyCTF 2026\
**Status:** Platform-confirmed

## Flag

``` text
spooky{m4yb3_1_n33d_t0_10v3_mys31f}
```

## Challenge

Di challenge ini gue dikasih sebuah binary ELF bernama `philophobia.bin`
dengan arsitektur x86-64 dan ukuran 16.512 bytes. Binary-nya belum
di-strip.

Saat dijalankan, program menampilkan puisi dan gambar hati, lalu meminta
input berupa dua angka (`start` dan `end`). Setelah itu, program meminta
satu baris yang berkaitan dengan petunjuk *"a certain famous summer
day"*.

Target gue adalah memahami validasi input di binary tersebut dan
menemukan flag yang disimpan di dalamnya.

## Solution

### 1. Identifikasi referensi Sonnet 18

Petunjuk *"a certain famous summer day"* mengarah ke **Sonnet 18** karya
William Shakespeare.

Baris pembukanya adalah:

``` text
Shall I compare thee to a summer's day?
```

Ini menjadi teks yang harus gue masukkan agar validasi pertama berhasil.

### 2. Analisis validasi input

Dari hasil analisis binary, program menerima dua angka, yaitu `start`
dan `end`.

Program kemudian menjalankan `strncmp` untuk membandingkan 20 byte input
yang dimulai dari offset `start` dengan string:

``` text
Shall I compare thee
```

Kalau cocok, program akan memanggil fungsi `print_flag`.

Di dalam fungsi tersebut, terdapat blob terenkripsi sepanjang 35 byte
yang di-XOR menggunakan key dengan rumus:

``` text
key = (end - start) + 71
```

### 3. Mencari XOR key

Karena format flag sudah diketahui diawali dengan `spooky{`, gue bisa
menggunakan known-plaintext attack sederhana.

Caranya adalah melakukan XOR antara plaintext yang sudah diketahui
(`spooky{`) dengan byte awal blob terenkripsi. Dari perhitungan
tersebut, didapatkan key:

``` text
90
```

Selanjutnya, masukkan nilai key ke rumus yang digunakan binary:

``` text
90 = (end - start) + 71
end - start = 90 - 71
end - start = 19
```

Jadi, selisih nilai `end` dan `start` harus 19. Gue menggunakan:

``` text
start = 0
end   = 19
```

### 4. Menjalankan binary

Jalankan binary dengan input berikut:

``` bash
./philophobia.bin
```

Masukkan angka:

``` text
0 19
```

Kemudian masukkan baris Sonnet 18:

``` text
Shall I compare thee to a summer's day?
```

Dengan kombinasi tersebut, validasi berhasil dan program menampilkan
flag.

## Flag

``` text
spooky{m4yb3_1_n33d_t0_10v3_mys31f}
```

Maknanya: **"maybe I need to love myself."**

Flag ini sudah dikonfirmasi melalui eksekusi binary dan diterima oleh
platform.
