mod_hex = ['c', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'r', 't', 'u', 'v']
original_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
d = dict(zip(mod_hex, original_hex))

input_modhex = "vvtcdjrlgldh"
output = ''.join((d[c]) for c in input_modhex)
print(output)


    
