import typing

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


def int_to_bitstring(n, length_bytes=None):
    if length_bytes is None:
        length_bytes = (n.bit_length() + 7) // 8
    b = n.to_bytes(length_bytes, 'big')
    return ''.join(f'{byte:08b}' for byte in b)


def rotr(x, n):
    return (x >> n) | (x << (32 - n))


def ch(x, y, z):
    return (x & y) ^ (~x & z)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def large_sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def large_sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def sha256(message: typing.Union[str, bytes, bytearray]):
    if isinstance(message, str):
        message = bytearray(message, 'ascii')
    elif isinstance(message, bytes):
        message = bytearray(message)

    H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

    length = len(message) * 8
    message.append(0x80)
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0x00)
    message += length.to_bytes(8, 'big')

    M = [message[i:i+64] for i in range(0, len(message), 64)]
    for M_i in M:
        W = [bytes(M_i[t*4:(t*4)+4]) for t in range(16)]
        for t in range(16, 64):
            W.append(
                (
                    (sigma1(int.from_bytes(W[t-2], 'big')) +
                    int.from_bytes(W[t-7], 'big') +
                    sigma0(int.from_bytes(W[t-15], 'big')) +
                    int.from_bytes(W[t-16], 'big')) & 0xFFFFFFFF
                ).to_bytes(4, 'big')
            )

        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]

        for t in range(64):
            T1 = (h + large_sigma1(e) + ch(e, f, g) + K[t] + int.from_bytes(W[t], 'big')) & 0xFFFFFFFF
            T2 = (large_sigma0(a) + maj(a, b, c)) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF

        H[0] = (a + H[0]) & 0xFFFFFFFF
        H[1] = (b + H[1]) & 0xFFFFFFFF
        H[2] = (c + H[2]) & 0xFFFFFFFF
        H[3] = (d + H[3]) & 0xFFFFFFFF
        H[4] = (e + H[4]) & 0xFFFFFFFF
        H[5] = (f + H[5]) & 0xFFFFFFFF
        H[6] = (g + H[6]) & 0xFFFFFFFF
        H[7] = (h + H[7]) & 0xFFFFFFFF

    return ''.join(f'{h:08x}' for h in H)


if __name__ == "__main__":
    print(sha256(input()))
