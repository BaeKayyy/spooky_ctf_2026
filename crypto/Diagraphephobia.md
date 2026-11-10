# Diagraphephobia — PDF Klingon yang Diredaksi

**Author soal:** Abhishek Kr Gupta  
**Event:** SpookyCTF 2026  
**Kategori:** Cryptography / PDF Forensics (Medium, 75 poin)  
**Status:** Flag berhasil ditemukan

## Flag

```text
spooky{qaStaH_nuq}
```

## Soal

Federasi nemuin sebuah file hasil penyadapan terhadap bangsa Klingon. File-nya berupa PDF satu halaman bernama `Diagraphephobia.pdf`.

Di dalam PDF ada tulisan `Ja'` (dalam bahasa Klingon artinya kurang lebih "tell" atau "report"), beberapa bagian yang ditutup black redaction bars, dan gambar yang kelihatan glitch. Tugasnya adalah membongkar isi informasi yang disembunyikan tersebut.

## File

- `challenge-files/Diagraphephobia.pdf` — PDF satu halaman yang berisi teks dan bagian yang diredaksi.

## Solusi

### 1. Cek isi PDF, jangan cuma lihat tampilannya

Awalnya PDF ini kelihatan seperti dokumen yang sudah disensor. Tapi ternyata redaction-nya cuma visual: teks aslinya masih tersimpan di text layer PDF.

Jadi, walaupun bagian tersebut ditutup kotak hitam, teks di baliknya masih bisa diekstrak. Dari hasil ekstraksi, ditemukan sebuah string Base64.

Intinya, jangan langsung menganggap teks yang ditutup hitam sudah benar-benar dihapus dari file PDF.

### 2. Cari petunjuk dari metadata PDF

Setelah teks Base64 ditemukan, bagian berikutnya adalah memeriksa metadata PDF.

Di field **Subject / Description**, ditemukan nilai:

```text
lojmIt yIpoSmoH!
```

Kalimat tersebut merupakan bahasa Klingon yang berarti **"Open the door!"**.

Yang menarik, panjang string tersebut tepat 16 karakter. Ini cocok dengan panjang key untuk AES-128, jadi string tersebut digunakan sebagai key dekripsi.

### 3. Decode Base64, lalu decrypt AES

String yang ditemukan dari text layer PDF masih berupa Base64. Decode dulu string tersebut untuk mendapatkan ciphertext, kemudian decrypt menggunakan algoritma **AES-128-ECB** dengan key:

```text
lojmIt yIpoSmoH!
```

Hasil dekripsinya berupa plaintext berbahasa Klingon. Teksnya diawali dengan:

```text
nuqneH
DaHjaj tlhIngan yotlh...
```

Flag juga ditemukan di dalam hasil plaintext tersebut.

### 4. Hasil akhir

Setelah proses dekripsi selesai, flag yang didapat adalah:

```text
spooky{qaStaH_nuq}
```

## Pelajaran

- **Redaction visual belum tentu menghapus data.** Teks yang ditutup kotak hitam bisa saja masih tersimpan di text layer PDF.
- **Periksa metadata file.** Informasi seperti Subject atau Description kadang menyimpan petunjuk penting untuk menyelesaikan challenge.
- **Perhatikan panjang key.** String `lojmIt yIpoSmoH!` memiliki panjang 16 karakter, sesuai dengan key AES-128.
- **Jangan berhenti di Base64.** Base64 hanya encoding, bukan enkripsi. Setelah decode, ciphertext masih perlu didekripsi menggunakan algoritma dan key yang tepat.

Flag berhasil ditemukan dari teks yang masih tertanam di PDF, lalu didekripsi menggunakan petunjuk dari metadata.
