base = 7
modulus = 20201227

def dlog(val, b=base, m=modulus):
    e = 0
    p = 1
    while True:
        e += 1
        p = (p * base) % m
        if p == val:
            return e

def main(data, part, log):
    door_pub, card_pub = [int(i) for i in data.read().strip().split('\n')]
    a = dlog(door_pub)
    b = dlog(card_pub)
    print('A', a, 'B', b)
    e = 1
    for i in range(a):
        e = (e * card_pub) % modulus
    print('E', e)