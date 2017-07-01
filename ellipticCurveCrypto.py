# y^2 = X^3 + ax + b (mod p)
a = 0x340E7BE2A280EB74E2BE61BADA745D97E8F7C300
b = 0x1E589A8595423412134FAA2DBDEC95C8D8675E58
p = 0xE95E4A5F737059DC60DFC7AD95B3D8139515620F

P = (0xBED5AF16EA3F6A4F62938C4631EB5AF7BDBCDBC3, 0x1667CB477A1A8EC338F94741669C976316DA6321)
d1 = 197919899782636687082760
d2 = 509549134202698380559908
d3 = d1 + d2
Q1 = (0x1FB51FFCE6640F43243FA866EBD022D91CFDE2D5, 0x3170B56C4E3400D9C1166BE99C049AEEF02699F0)
Q2 = (0x7E638858BA98C384C6837B1508A774801F1E96B0, 0x8979E33A8A0E36A3193D79DAE55A19E0F9287FCA)


def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0
    d, s, t = extended_euclid(b, a % b)
    d, s, t = (d, t, s - (a // b) * t)
    return d, s, t


def modinv(a, n):
    d, s, _ = extended_euclid(a, n)
    if d == 1:
        return s % n


def add(A, B):
    # adding neutral element
    if A == 'x':
        return B
    elif B == 'x':
        return A

    xa, ya = A[0], A[1]
    xb, yb = B[0], B[1]

    # adding point to itself
    if xa == xa and ya == yb:
        return double(A)

    u = ((yb - ya) * modinv(xb - xa, p)) % p
    xc = u ** 2 - xa - xb
    yc = -ya - u * (xc - xa)
    return xc % p, yc % p


def double(A):
    #doubling neutral element
    if A == 'x':
        return A

    xa, ya = A[0], A[1]
    u = ((3 * (xa ** 2) + a) * modinv(2 * ya, p)) % p
    xc = u ** 2 - 2 * xa
    yc = -ya - u * (xc - xa)
    return xc % p, yc % p


'''
ouble_and_add:
A * 5 = A * 101(binary)

1 -> A + A = 2A
0 -> 2A * 2
1 -> 2A * 2 + A = 4A + A = 5A
'''
def multiply(k, P):
    Q = 'x'
    bits = "{0:b}".format(k)
    for bit in bits:
        Q = double(Q)
        if bit == '1':
            Q = add(Q, P)
    return Q


q1 = multiply(d1, P)
print("d1 * P = {}".format(q1))
print("= Q1 = {} ".format(Q1))
print()

q2 = multiply(d2, P)
print("d2 * P = {}".format(q2))
print("= Q2 = {} ".format(Q2))
print()

Q3 = add(Q1, Q2)
q3 = multiply(d3, P)
print("Q1 + Q2 = (d1 + d2) * P")
print("{} = {} ".format(q3, Q3))