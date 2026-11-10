#!/usr/bin/env python3

ciphertext = ( "Etu_taip5_w5n_hpmnw_hlgsdso{lyh0_d}"
"jyi_piihef_ne_oy3p0lh4oskt_i:k3l3" )

def rail_fence_decrypt(cipher: str, rails: int) -\> str: if rails \< 2:
return cipher

    n = len(cipher)
    pattern = []
    row = 0
    direction = 1

    # Recreate the zigzag rail pattern.
    for _ in range(n):
        pattern.append(row)

        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1

        row += direction

    # Count how many characters belong to each rail.
    counts = [pattern.count(i) for i in range(rails)]

    # Split the ciphertext into its rail segments.
    rail_chars = []
    pos = 0

    for count in counts:
        rail_chars.append(list(cipher[pos:pos + count]))
        pos += count

    # Reconstruct the plaintext by following the zigzag pattern.
    plaintext = []

    for rail in pattern:
        plaintext.append(rail_chars[rail].pop(0))

    return "".join(plaintext)

if **name** == "**main**": plaintext = rail_fence_decrypt(ciphertext, 4)

    print("[+] Decrypted plaintext:")
    print(plaintext)

    flag = plaintext.split(":", 1)[-1]
    print("\n[+] Flag:")
    print(flag)
