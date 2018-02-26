alphabetic = '0123456789abcdefghijklmnopqrstuvwxyz'

def transform(x, n, digits = None):
    if digits is None:
        digits = alphabetic
    result = ''
    while x:
        result = digits[x % n] + result
        x //= n
    return result

def count_digit(x, n, d):
    k = 0
    while x > 0:
        if x % n == d:
            k += 1
        x //= n
    return k

if __name__ == "__main__":
    s = input('Enter source number and its radix [optional]: ')
    if len(s.split()) == 1:
        x = int(s)
    elif len(s.split()) == 2:
        x, base = s.split()
        x = int(x, int(base))
    else:
        raise RuntimeError("Expected one or two parameters!")

    s = input('Enter target radix and desired digit [optional]: ')
    if len(s.split()) == 1:
        n, k = int(s), None
    elif len(s.split()) == 2:
        n, k = s.split()
        n = int(n)
    else:
        raise RuntimeError("Expected one or two parameters!")

    y = transform(x, n)
    print('Source number in target radix is {}.'.format(y))
    if k is not None:
        print('Desired digit met {} times'.format(y.count(k)))
