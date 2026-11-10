# Phantom Login — Forensik Windows Log

**Author soal:** Abhishek Kr Gupta  
**Event:** SpookyCTF 2026  
**Kategori:** Digital Forensics / Windows Log Analysis (Medium, 75 poin)  
**Status:** Flag berhasil ditemukan

## Flag

```text
spooky{the_ghost_left_a_trace}
```

## Soal

Di challenge ini, kita dikasih sebuah bundle log bernama `Phantom_Login.zip`. Ceritanya ada akun misterius yang seharusnya sudah lama dilupakan, tapi tiba-tiba muncul dan berhasil login ke sistem NJIT. Setelah itu, akun tersebut mengakses direktori arsip.

Tugasnya adalah menelusuri aktivitas akun tersebut dari Windows Security Log dan web access log, lalu menemukan flag yang ditinggalkan.

## File

- `challenge-files/Phantom_Login.zip` — bundle log yang berisi `njit_security.csv`, `njit_web.log`, `case_notes.txt`, dan `PLAYER_README.md`.
- `evidence/phantom_case_notes.txt` — catatan tambahan terkait kasus.

## Solusi

### 1. Cari akun yang mencurigakan

Pertama, fokus ke Windows Security Log dan cari aktivitas login yang kelihatan nggak biasa.

Dari hasil pemeriksaan, akun `evelyn.graves` paling mencurigakan. Akun ini merupakan satu-satunya user yang tercatat mengakses sistem dari IP eksternal `203.0.113.77`.

Timeline aktivitasnya pada 31 Oktober 2026 (UTC):

| Waktu (UTC) | Event ID | Aktivitas |
|---|---:|---|
| 03:10–03:12 | 4625 | 9 kali login gagal |
| 03:14 | 4624 | Login berhasil |
| 03:15 | 4672 | Mendapatkan special privileges |
| 03:17 | 5140 | Mengakses `\\BW-FS01\Archives$` |

Semua aktivitas tersebut menggunakan LogonID yang sama, yaitu `0xB130`. Ini penting karena membantu menghubungkan rangkaian event tersebut sebagai satu sesi aktivitas.

Ada juga beberapa login gagal dari akun `administrator` melalui IP `198.51.100.66`. Namun, itu cuma pengalih perhatian karena akun dan IP sumbernya berbeda dari aktivitas `evelyn.graves`.

### 2. Hubungkan dengan web access log

Setelah akun dan IP mencurigakan ditemukan di Security Log, lanjut periksa `njit_web.log`.

Di sana terlihat user dan IP yang sama mengakses endpoint:

```text
/archives/
/archives/export?note=...
```

Aktivitas ini nyambung dengan event 5140 sebelumnya, yaitu ketika akun tersebut mengakses network share `\\BW-FS01\Archives$`.

Jadi, fokus investigasi berikutnya ada di parameter `note` pada endpoint `/archives/export`.

### 3. Decode parameter `note`

Nilai parameter `note` ternyata menggunakan Base64. Tinggal ambil nilainya, lalu decode untuk mendapatkan isi aslinya.

Contoh perintah di terminal:

```bash
echo 'ISI_PARAMETER_NOTE' | base64 -d
```

Hasil decode tersebut adalah flag challenge:

```text
spooky{the_ghost_left_a_trace}
```

## Pelajaran

- **Korelasi event itu penting.** Jangan cuma melihat satu event secara terpisah. LogonID `0xB130` membantu menghubungkan login berhasil, pemberian privilege, dan akses network share.
- **Perhatikan akun dan IP sumber.** Aktivitas `evelyn.graves` dari `203.0.113.77` menjadi petunjuk utama, sedangkan kegagalan login `administrator` dari IP lain merupakan decoy.
- **Gabungkan bukti dari beberapa log.** Windows Security Log menunjukkan aktivitas autentikasi dan akses share, sedangkan web access log memperlihatkan endpoint yang diakses.
- **Base64 bukan enkripsi.** Parameter `note` hanya perlu di-decode untuk mendapatkan flag.

Flag ditemukan dengan menghubungkan aktivitas akun `evelyn.graves` di Windows Security Log dengan request pada web access log, lalu men-decode parameter `note`.
