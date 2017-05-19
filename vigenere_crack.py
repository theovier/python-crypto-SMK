import string
import collections
import queue

ASCII_OFFSET = 97


def get_alphabetical_index(char):
    return ord(char) - ASCII_OFFSET


def get_char_occurrences(text):
    occurrences = {}
    for letter in string.ascii_lowercase:
        occurrences.__setitem__(letter, 0)
    for c in filtered_text_encoded:
        occurrence = occurrences.__getitem__(c)
        occurrences.__setitem__(c, occurrence + 1)
    return occurrences


def get_koinzidenz_index(text):
    n = len(text)
    occurrences = get_char_occurrences(filtered_text_encoded)
    x = 1 / (n * (n - 1))
    accumulation = 0
    for letter in string.ascii_lowercase:
        occurrence = occurrences.get(letter)
        accumulation += occurrence * (occurrence - 1)
    return x * accumulation


def get_key_length(text):
    koinzidenz_index_random = 0.0385
    koinzidenz_index_english = 0.068
    n = len(filtered_text_encoded)
    i = get_koinzidenz_index(filtered_text_encoded)
    k = ((koinzidenz_index_english - koinzidenz_index_random) * n) / ((n - 1) * i - koinzidenz_index_random * n + koinzidenz_index_english)
    return k


def encrypt_caesar(text, shift):
    encryption = ""
    for i in range(len(text)):
        alphabetical_char_index = get_alphabetical_index(text[i])
        shifted_alphabetical_char_index = (alphabetical_char_index + shift) % 26
        encryption += chr(shifted_alphabetical_char_index + ASCII_OFFSET)
    return encryption


'''
cracks the shift for every group with the same shifting.
'''
def crack_groups(shift_groups):
    decoded_groups = []
    for text in shift_groups:
        most_frequent_char = collections.Counter(text).most_common(1)[0][0]
        shift = get_alphabetical_index(most_frequent_char) - get_alphabetical_index('e')
        decoded_group = encrypt_caesar(text, -shift)
        decoded_groups.append(decoded_group)
    return decoded_groups


'''
input=>
['sc...']
['eu...']
['cr...']
['ri...']
['et...']
['cy...']
['ya...']
['sn...']
['ed...']

output=>
['secrecyse']
['curityand']
['obscurity']

input => k = 3, blocks:
['a', 'b', 'c']
['d', 'e', 'f']
['g', 'h']

output => 
['a', 'd', 'g']
['b', 'e', 'h']
['c', 'f']
...
'''
def rotate_right(blocks, k):
    liste = []
    for i in range(k):
        item = ""
        for block in blocks:
            if i < len(block):
                item += block[i]
        liste.append(item)
    return liste


def get_char_queue(text):
    q = queue.Queue()
    for c in text:
        q.put(c)
    return q


def format_output(formatted_text, decoded_text):
    queue = get_char_queue(decoded_text)
    msg = ""
    for c in formatted_text:
        if c in string.ascii_lowercase:
            msg += queue.get()
        else:
            msg += c
    return msg


text_encoded = open('../resources/geheimtext.txt', encoding="utf-8").read()
filtered_text_encoded = ''.join(c for c in text_encoded if c in string.ascii_lowercase)

k = get_key_length(filtered_text_encoded)
print("Koinzidenzindex: {}".format(k))
k = round(k)
print("Koinzidenzindex (gerundet): {}".format(k))
print()

blocks = [filtered_text_encoded[i: i + k] for i in range(0, len(filtered_text_encoded), k)]
print("Anzahl an Blocks: {} ({} / {})".format(len(blocks), len(filtered_text_encoded),k ))

groups_with_same_shift = rotate_right(blocks, k)
cracked_groups = crack_groups(groups_with_same_shift) # k-Reihen; #Blocks Characters pro Reihe
decoded_blocks = rotate_right(cracked_groups, len(blocks))
decrypt = ''.join(decoded_blocks)
formatted_decoded_text = format_output(text_encoded, decrypt)

for x in blocks:
    print(x)
print()

for x in groups_with_same_shift:
    print(x)
print()

for x in cracked_groups:
    print(x)
print()

for x in decoded_blocks:
    print(x)
print()

print(formatted_decoded_text)
