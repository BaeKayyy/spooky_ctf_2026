# Heads will Roll

**- Category:** Cryptography

## Solution

### 1. Cipher Identification

From the challenge description, there are several hints pointing to the
**Rail Fence Cipher**:

-   "Rolling, rolling" refers to the zigzag pattern.
-   "Near the rails" directly hints at Rail Fence.
-   "Through the air" reinforces the movement between rails.

Based on these clues, I identified Rail Fence as the encryption method.

### 2. Ciphertext Analysis

After opening `pumpkin_head_message.txt`, I found the following
ciphertext:

``` text
Etu_taip5_w5n_hpmnw_hlgsdso{lyh0_d}jyi_piihef_ne_oy3p0lh4oskt_i:k3l3
```

The next step was to decrypt it using Rail Fence with 4 rails.

### 3. Decryption

I used a Python script to reconstruct the zigzag pattern and recover the
original message. The solver is provided separately in
`heads_will_roll_solver.py`.

### 4. Flag Recovery

After successfully decrypting the ciphertext, the plaintext was:

``` text
Enjoy_this_pumpkin_with_the_flag_inside:_spooky{5l33py_h0ll0w_h34d5}
```

The flag was located at the end of the decrypted message.

**Flag:**

``` text
spooky{5l33py_h0ll0w_h34d5}
```
