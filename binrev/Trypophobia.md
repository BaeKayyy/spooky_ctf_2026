# Trypophobia — Reverse Engineering Java Class

**Author soal:** Ryan  
**Event:** SpookyCTF 2026  
**Kategori:** Reverse Engineering (Java Bytecode, 96 poin)  
**Status:** Flag ditemukan dan terverifikasi

## Flag

```text
spooky{ever_reversed_java?A67b_91}
```

## Soal

Dikasih satu file bernama `binary`. Setelah dicek pakai perintah `file`, ternyata file tersebut bukan ELF, melainkan **Java class** versi 52 (Java 8).

Program bisa dijalankan menggunakan:

```bash
java binary <flag>
```

Output-nya berupa `Correct!` atau `Incorrect.`. Format flag yang digunakan adalah `spooky{...}`.

Tugasnya adalah mencari input yang membuat program mengeluarkan `Correct!`.

## File

- `challenge-files/binary` — Java class yang harus dianalisis.

## Solusi

### 1. Identifikasi file dan bongkar bytecode

Kalau file dibuka menggunakan text editor, isinya hanya terlihat seperti data biner. Karena itu, gue memeriksa tipe file terlebih dahulu:

```bash
file binary
```

Hasilnya menunjukkan bahwa file tersebut merupakan Java class, bukan executable ELF. Selanjutnya, bytecode dibongkar menggunakan:

```bash
javap -c -p binary.class
```

Decompiler seperti CFR atau JADX juga bisa digunakan, tetapi `javap` sudah cukup untuk menganalisis challenge ini.

### 2. Analisis fungsi `check()`

Di fungsi `check()`, program pertama-tama memeriksa panjang input harus tepat **34 karakter**. Pemeriksaan ini terlihat dari instruksi `bipush 34` yang diikuti `if_icmpne`.

Setelah pemeriksaan panjang, terdapat 34 blok validasi yang bentuknya mirip. Setiap blok mengambil karakter pada indeks tertentu menggunakan `charAt(i)`, memprosesnya dengan beberapa operasi integer, lalu membandingkan hasilnya dengan sebuah konstanta. Jika hasilnya tidak cocok, program akan menuju `return false`.

Karena setiap karakter diperiksa secara independen, seluruh flag tidak perlu ditebak sekaligus. Persamaan pada masing-masing blok bisa dibalik satu per satu untuk mendapatkan karakter aslinya.

### 3. Baca operasi pada JVM stack

JVM merupakan *stack machine*, jadi saat membaca bytecode, isi stack harus dilacak. Misalkan `c` adalah karakter pada indeks ke-`i`. Ada tiga pola operasi yang berulang berdasarkan `i mod 3`.

| `i mod 3` | Bentuk bytecode | Persamaan (`T` = konstanta pembanding) | Bentuk invers |
|---:|---|---|---|
| 0 | `push K; swap; ixor; dup; pop; push A; iadd` | `(K ^ c) + A = T` | `c = (T - A) ^ K` |
| 1 | `push K; swap; isub; push X; ixor` (pada beberapa blok diikuti `iadd`) | `(K - c) ^ X = T` (atau bentuk dengan `+ X`) | `c = K - (T ^ X)` (atau `K - (T - X)`) |
| 2 | `dup; push A; iadd; swap; pop; push X; ixor` | `(c + A) ^ X = T` | `c = (T ^ X) - A` |

Operator `^` berarti XOR. Instruksi `dup; pop` hanya menjadi pengecoh karena tidak mengubah nilai yang sedang diproses.

Hal yang perlu diperhatikan adalah instruksi `swap` sebelum `isub`. Urutan stack membuat operasi yang dilakukan menjadi `K - c`, bukan `c - K`.

Beberapa konstanta pembanding (`T`) bernilai negatif, misalnya `-46`. Ini normal karena integer pada JVM menggunakan representasi signed 32-bit. Operasi XOR dengan bilangan negatif tetap bisa dihitung menggunakan Python atau kalkulator dalam mode programmer.

### 4. Balik persamaan untuk mendapatkan karakter

Berikut tiga contoh perhitungan dari indeks awal.

**Indeks 0 — pola 0**

Persamaannya:

```text
(31 ^ c) + 7 = 115
```

Balik persamaannya:

```text
31 ^ c = 115 - 7
31 ^ c = 108
c = 108 ^ 31
c = 115
```

Nilai ASCII `115` adalah karakter `s`.

**Indeks 1 — pola 1**

Persamaannya:

```text
(73 - c) ^ 11 = -46
```

Balik persamaannya:

```text
73 - c = -46 ^ 11
73 - c = -39
c = 112
```

Nilai ASCII `112` adalah karakter `p`.

**Indeks 2 — pola 2**

Persamaannya:

```text
(c + 5) ^ 22 = 98
```

Balik persamaannya:

```text
c + 5 = 98 ^ 22
c + 5 = 116
c = 111
```

Nilai ASCII `111` adalah karakter `o`.

Tiga karakter pertama menghasilkan `spo`, sesuai dengan awalan format flag `spooky{}`. Ini menjadi indikasi bahwa pembacaan stack dan pembalikan persamaan sudah benar.

### 5. Susun seluruh karakter

Proses yang sama diterapkan ke seluruh 34 blok validasi. Hasilnya:

| Indeks | Persamaan | `T` | Karakter |
|---:|---|---:|---|
| 0 | `(31 ^ c) + 7` | 115 | `s` (115) |
| 1 | `(73 - c) ^ 11` | -46 | `p` (112) |
| 2 | `(c + 5) ^ 22` | 98 | `o` (111) |
| 3 | `(19 - c) + 51` | -41 | `o` (111) |
| 4 | `(94 ^ c) + 13` | 66 | `k` (107) |
| 5 | `(37 - c) ^ 23` | -69 | `y` (121) |
| 6 | `(c + 17) ^ 12` | 128 | `{` (123) |
| 7 | `(3 - c) + 83` | -15 | `e` (101) |
| 8 | `(41 ^ c) + 29` | 124 | `v` (118) |
| 9 | `(66 - c) ^ 9` | -44 | `e` (101) |
| 10 | `(c + 21) ^ 9` | 142 | `r` (114) |
| 11 | `(15 - c) + 55` | -25 | `_` (95) |
| 12 | `(88 ^ c) + 27` | 69 | `r` (114) |
| 13 | `(14 - c) ^ 31` | -74 | `e` (101) |
| 14 | `(c + 7) ^ 79` | 50 | `v` (118) |
| 15 | `(25 - c) + 33` | -43 | `e` (101) |
| 16 | `(61 ^ c) + 11` | 90 | `r` (114) |
| 17 | `(27 - c) ^ 17` | -71 | `s` (115) |
| 18 | `(c + 13) ^ 48` | 66 | `e` (101) |
| 19 | `(25 - c) + 88` | 13 | `d` (100) |
| 20 | `(32 ^ c) + 9` | 136 | `_` (95) |
| 21 | `(69 - c) ^ 28` | -57 | `j` (106) |
| 22 | `(c + 12) ^ 13` | 96 | `a` (97) |
| 23 | `(31 - c) + 50` | -37 | `v` (118) |
| 24 | `(87 ^ c) + 15` | 69 | `a` (97) |
| 25 | `(31 - c) ^ 34` | -62 | `?` (63) |
| 26 | `(c + 18) ^ 68` | 23 | `A` (65) |
| 27 | `(37 - c) + 12` | -5 | `6` (54) |
| 28 | `(49 ^ c) + 21` | 27 | `7` (55) |
| 29 | `(86 - c) ^ 5` | -15 | `b` (98) |
| 30 | `(c + 24) ^ 30` | 105 | `_` (95) |
| 31 | `(8 - c) + 67` | 18 | `9` (57) |
| 32 | `(11 ^ c) + 27` | 85 | `1` (49) |
| 33 | `(48 - c) ^ 11` | -72 | `}` (125) |

Jika semua karakter digabungkan sesuai urutan indeks, diperoleh:

```text
spooky{ever_reversed_java?A67b_91}
```

### 6. Verifikasi flag

Flag yang sudah disusun kemudian diuji langsung menggunakan Java class aslinya:

```bash
java binary 'spooky{ever_reversed_java?A67b_91}'
```

Output program:

```text
Correct!
```

Dengan demikian, flag berhasil diverifikasi menggunakan binary asli.

## Pelajaran

- **Kenali format file terlebih dahulu.** File bernama `binary` belum tentu executable ELF. Perintah `file` membantu menentukan alat analisis yang tepat.
- **Gunakan `javap` untuk membaca bytecode.** Untuk challenge Java sederhana, `javap -c -p` sudah bisa memperlihatkan instruksi dan alur validasi tanpa harus memakai decompiler.
- **Pahami urutan operand pada stack.** Instruksi seperti `swap` dan `isub` berpengaruh terhadap urutan operasi. Salah membaca urutan operand bisa menghasilkan karakter yang keliru.
- **Balik operasi, bukan menebak flag.** Karena setiap indeks divalidasi secara independen, persamaan tiap karakter dapat diselesaikan secara terpisah.
- **Verifikasi ke program asli.** Hasil ekstraksi belum dianggap selesai sebelum input menghasilkan output `Correct!`.

Flag ditemukan dengan membalik validasi pada Java bytecode dan dikonfirmasi melalui eksekusi class aslinya.
