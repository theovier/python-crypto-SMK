#k = k' = Y^x mod p = X^y mod p
p = 323453257
g = 2345149
X = 205125783 # X = g^x mod p
Y = 71774435 # Y = g^y mod p


def bruteforce_y(g, p, Y):
    y = 0
    while True:
        Y_Clone = pow(g, y, p)
        if Y_Clone == Y:
            return y
        y += 1


def bruteforce_x(g, p, X):
    x = 0
    while True:
        X_Clone = pow(g, x, p)
        if X_Clone == X:
            return x
        x += 1


x = 36503778 #bruteforce_x(g, p, X)
y = 131619160 #bruteforce_y (g, p, Y)

k1 = pow(X, y, p)
k2 = pow(Y, x, p)
print("k = k' = {} = {}".format(k1, k2)) #255184310



