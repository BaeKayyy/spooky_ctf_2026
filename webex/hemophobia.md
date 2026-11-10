# Hemophobia --- Roots Bloody Roots

**Category:** Web / OSINT\
**Author:** flamboy_ant\
**Difficulty:** Easy\
**Points:** 50

## Challenge Description

> You are trapped in this endless nightmare with music and blood seeping
> in through the ceiling, crawling down the walls. Once the blood
> reaches the bottom, your feet become rooted to the ground as the blood
> consumes you, and you relive it all over again. To escape you must
> find the key hidden within these walls, and only then can you escape
> this nightmare. Goodluck...

## Solving the Challenge

### Step 1 --- Exploring the Website

Pertama, gue buka website yang diberikan di challenge:

<http://77.112.83.127>

Di halaman utama, terlihat animasi darah yang turun dari langit-langit,
countdown, dan form untuk memasukkan flag.

Ada satu petunjuk menarik di bagian halaman:

> Someone left a note in the walls of this page. Pages are made of text,
> and you are allowed to read all of it.

Menurut gue, kalimat **"walls of this page"** mengarah ke source code
halaman web. Jadi, gue lanjut memeriksa HTML melalui **View Page
Source** atau Developer Tools.

Di dalam source code, gue menemukan komentar HTML berikut:

``` html
<!-- There's a song that plays in this nightmare, but it's no longer here...
I wrote it down somewhere though. I think it's in nightmare.txt...
The flag looks like spooky{band} -->
```

Dari komentar tersebut, ada dua informasi penting:

1.  Ada file bernama `nightmare.txt` yang kemungkinan bisa diakses
    langsung dari server.
2.  Format flag yang diminta adalah `spooky{band}`, sehingga jawaban
    yang dicari merupakan nama sebuah band.

### Step 2 --- Reading `nightmare.txt`

Berbekal petunjuk tadi, gue mencoba membuka file tersebut secara
langsung:

<http://77.112.83.127/nightmare.txt>

Di dalam file `nightmare.txt`, terdapat petunjuk berupa judul lagu
**Roots Bloody Roots**, disertai pertanyaan:

> Who made it?

Artinya, kita perlu mencari tahu siapa band yang membawakan lagu
tersebut.

### Step 3 --- Identifying the Band

Selanjutnya, gue mencari judul lagu **Roots Bloody Roots** melalui
Google.

Dari hasil pencarian, diketahui bahwa lagu tersebut merupakan lagu dari
band **Sepultura**, yang dirilis dalam album *Roots* pada tahun 1996.

Dengan begitu, nama band yang dibutuhkan untuk menyusun flag adalah
`Sepultura`.

### Step 4 --- Submitting the Flag

Sebelumnya, komentar HTML sudah memberikan format flag:

``` text
spooky{band}
```

Karena band yang ditemukan adalah Sepultura, flag yang gue gunakan:

``` text
spooky{Sepultura}
```

Website melakukan normalisasi input menggunakan `toLowerCase()` sebelum
memvalidasi hash, sehingga penggunaan huruf kapital pada nama band tidak
memengaruhi validasi.

## Flag

``` text
spooky{Sepultura}
```

## Bonus Track

Buat yang penasaran sama lagunya, ini link Spotify **Roots Bloody
Roots** dari Sepultura:

[Listen on
Spotify](https://open.spotify.com/track/6ursmCnbc9oDRGa2yHKkoZ?si=1fac3f10d10d482b)

## Conclusion

Challenge Hemophobia bisa diselesaikan dengan melakukan pemeriksaan
source code halaman web, menemukan petunjuk file `nightmare.txt`, lalu
mengidentifikasi band dari judul lagu yang diberikan.

Teknik utama yang digunakan adalah **source code inspection** dan
**OSINT sederhana**. Jadi, kuncinya bukan mengeksploitasi animasi atau
mekanisme countdown, melainkan memperhatikan petunjuk yang sengaja
ditinggalkan oleh pembuat challenge.
