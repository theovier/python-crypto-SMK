import hashlib


def generate_hash(data):
    return hashlib.sha1(data).hexdigest()


def generate_hmac(key, msg):
    block_size = 64
    if (len(key) > block_size):
        key = generate_hash(key)

    if (len(key) < block_size):
        key = key.ljust(block_size, b'\0')

    ipad = bytearray((x ^ 0x36) for x in key)
    opad = bytearray((x ^ 0x5c) for x in key)

    #append msg to ipad
    for byte in msg:
        ipad.append(byte)

    inner_hash = generate_hash(ipad)

    #append inner_hash to opad
    [opad.append(byte) for byte in bytearray.fromhex(inner_hash)]

    return generate_hash(opad)


#http://blog.gingerlime.com/2010/once-upon-a-time/
def get_HOTP(hmac_hex, d):
    i = int(hmac_hex[-1], 16) #last hex char
    '''
    select the 4 bytes determined by i, i+1, i+2, i+3
    i*2, because our 20 byte hmac-sha1-hash is 40 characters long.
    +8, because we need 4 bytes, which are represented by 4*2 characters.
    for i = 10, its the same as: hmac_hex[20:28].
    '''
    target_bytes_in_hex = hmac_hex[(i * 2):((i * 2) + 8)] #e.g. 0x50ef7f19
    target_bytes = int(target_bytes_in_hex, 16)
    b31 = target_bytes & 0x7FFFFFFF
    return str(b31)[-d:]


def get_HOTP_byte_style(hmac_hex, d):
    hmac_bytes = bytearray.fromhex(hmac_hex)
    i = hmac_bytes[19] & 0x0F

    #select 4 Bytes
    first_byte = hex((hmac_bytes[i] & 0x7f) << 24 )  #e.g. 0x50000000
    second_byte = hex(hmac_bytes[i+1] << 16)         #e.g. 0xef0000
    third_byte = hex(hmac_bytes[i+2] << 8)           #e.g. 0x7f00
    fourth_byte = hex(hmac_bytes[i+3])               #e.g. 0x19

    # e.g. 0x50ef7f19
    selected_bytes_concatenated = int(first_byte, 16) +\
                                  int(second_byte, 16) + \
                                  int(third_byte, 16) + \
                                  int(fourth_byte, 16)

    #clear the highest bit
    b31 = selected_bytes_concatenated & 0x7FFFFFFF

    # only get the last d digits
    return b31 % (10 ** d)


if __name__ == '__main__':
    secret = "62 a0 9c 82 ee bf a0 32 3b 9c 76 da 18 2e 1f f8 5a 58 a2 d5"
    k = bytearray.fromhex(secret)
    c = bytes([0, 0, 0, 0, 0, 0, 0, 0])

    hmac_sha1 = generate_hmac(k, c)

    hotp = get_HOTP(hmac_sha1, 6)
    print(hotp)

    hotp = get_HOTP_byte_style(hmac_sha1, 6)
    print(hotp)









