# Cleithrophobia — pcap Star Trek

**Author soal:** Raindrops095
**Event:** SpookyCTF 2026
**Kategori:** Wireshark Network Traffic Analysis (Medium, 75 poin)
**Status:** Flag ketemu

## Flag

```
Spooky{Be0m_Me_Up_Sc0tty_2266}
```

Catatan: wrapper flag-nya pakai `S` kapital (`Spooky{...}`), bukan `spooky{...}` huruf kecil kayak biasanya. Jangan sampai salah ketik pas submit.

## Soal

Dikasih satu file packet capture, `Cleithrophobia.pcap` (2.000 paket), temanya kapal Starship Enterprise. Ceritanya kita kejebak di kapal yang mati total, dan disuruh nyari cara buat nyalain kapalnya dari file pcap ini.

## File

- `challenge-files/Cleithrophobia.pcap` — capture-nya

## Solusi

**1. Buang noise dulu.**
Hampir semua isi pcap ini cuma pengalih perhatian: trafik TLS, login FTP berulang buat scotty, sulu, spock, mccoy dan kru lainnya, ICMP, DNS, NTP, plus nilai `warp_core_telemetry` / `deflector` random yang nggak ada artinya. Semua login FTP-nya juga cuma dijawab `230 Access granted`, jadi nggak ada yang perlu dikulik di situ.

**2. Cari percobaan ignition.**
Dari deskripsi soal ("start the ship"), endpoint yang paling masuk akal itu `POST /bridge/ignition`. Gue filter di Wireshark:

```
http.request.method == "POST" && http.request.uri contains "ignition"
```

Ketemu 20 request, semuanya pakai HTTP Basic Auth. Header `Authorization: Basic ...` itu cuma Base64 dari `user:password`, jadi tinggal decode. Dari 20 percobaan, 19 dijawab `401 IGNITION DENIED`. Cuma satu yang lolos, yaitu akun `captain.kirk:Enterprise-1701-A` (frame 404), dan dijawab `200 OK - IGNITION AUTHORIZED - WARP CORE PREPARING` (frame 405).

Kredensial lainnya cuma jebakan: user-nya bener tapi password-nya salah (`captain.kirk:Enterprise-1701`, tanpa `-A`), atau password-nya bener tapi user-nya salah (`ops.bridge:Enterprise-1701-A`).

**3. Rakit flag-nya.**
Respons sukses itu bawa tiga header yang isinya potongan flag dalam Base64:

```
X-Bridge-Telemetry:  deflector_part1=U3Bvb2t5e0JlMA==
X-Deflector-Status:  deflector_part2=bV9NZV9VcF9TYw==
X-Warp-Core-Reading: deflector_part3=MHR0eV8yMjY2fQ==
```

Decode satu-satu terus sambung sesuai urutan:

- part1 → `Spooky{Be0`
- part2 → `m_Me_Up_Sc`
- part3 → `0tty_2266}`

Atau langsung di terminal:

```bash
for s in U3Bvb2t5e0JlMA== bV9NZV9VcF9TYw== MHR0eV8yMjY2fQ==; do echo -n $s | base64 -d; done; echo
```

Hasilnya:

```
Spooky{Be0m_Me_Up_Sc0tty_2266}
```

## Pelajaran

- Baca deskripsi soal dulu buat nentuin apa yang dicari. "Start the ship" langsung ngarah ke `/bridge/ignition`, jadi ratusan paket lain bisa dilewatin.
- Di trafik HTTP, bandingin respons yang gagal sama yang berhasil. Satu respons beda (status 200 plus header tambahan) di antara 19 respons 401 itu petunjuknya.
- Flag yang dipecah ke beberapa header nggak bakal ketemu pakai `strings | grep Spooky`, jadi baca isi respons yang relevan, jangan cuma nyari kata kunci.
- Basic Auth itu cuma Base64, bukan enkripsi. Kalau lewat HTTP biasa tanpa TLS, siapa pun yang nyadap bisa baca user dan password-nya.

Flag ketemu pas event.