# Arachnophobia

- **Category:** Forensics


## Solution

### 1. Static Analysis
Running `strings` on the image revealed `flag.txt` near the end of the binary data, indicating a hidden ZIP archive appended to the image file.

### 2. Extraction & Flag Recovery
Unzipped the image file directly and read the flag:

```bash
unzip image.png
cat flag.txt