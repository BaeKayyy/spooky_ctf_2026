# The Haunted Portrait

**- Category:** Steganography

## Solution

### 1. Initial Image Analysis

The challenge provides an image named `haunted_portrait.png`. I started
by checking common places where information could be hidden, such as
metadata and data appended after the PNG end.

There was no trailing data after the PNG end and no useful metadata, so
the investigation continued by examining the image pixels.

### 2. LSB Analysis

I checked the Least Significant Bit (LSB) planes of the RGB channels.

The Red and Green channels looked random, with approximately 50% of
their bits set to `1`. However, the Blue channel was different: only
around 3.6% of its LSBs were `1`, and those bits were concentrated
around the portrait region.

This indicated that the hidden message was stored in the Blue channel's
LSB plane.

### 3. Extracting the Hidden Message

After extracting the Blue-channel LSB plane, the hidden text became
visible:

``` text
THE PORTRAIT WHISPERS:
THE DEAD SPEAK IN ROT13
fcbbxl{cbegenvgf_xrrc_frpergf}
```

The message explicitly mentions ROT13, which indicates the encoding used
for the final line.

### 4. ROT13 Decoding

I decoded the final line using ROT13:

``` text
fcbbxl{cbegenvgf_xrrc_frpergf}
```

Decoded result:

``` text
spooky{portraits_keep_secrets}
```

### 5. Flag

The recovered flag is:

``` text
spooky{portraits_keep_secrets}
```
