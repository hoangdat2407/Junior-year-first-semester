# Modular exponentiation
def mod_exp(a, b, m):
    result = 1
    a = a % m
    while b > 0:
        if b % 2 == 1:     
            result = (result * a) % m
        a = (a * a) % m      
        b //= 2              
    return result

# Check is prime number
def is_prime(n):
    """Kiểm tra n có phải số nguyên tố hay không"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
#
# Mã hóa tên sang số nguyên (cơ số 27)
def name_encrypt(name: str, k: int = 27) -> int:
    if k < 27:
        k += 26
    name = name.upper()
    m = 0
    for char in name:
        if 'A' <= char <= 'Z':
            m = m * k + (ord(char) - ord('A') + 1)  # A=1..Z=26
    return m

# ================================================================================🔓 Giải mã số nguyên về tên=============================================================================
def name_decrypt(m: int, k: int = 27) -> str:
    if k < 27:
        k += 26
    if m == 0:
        return ""  # chuỗi rỗng

    chars = []
    while m > 0:
        digit = m % k
        if not (1 <= digit <= 26):
            raise ValueError(f"Giá trị {digit} không hợp lệ (ngoài 1..26)")
        chars.append(chr(digit - 1 + ord('A')))
        m //= k
    return ''.join(reversed(chars))

#=================================================== Tính nghịch đảo modulo sử dụng thuật toán Euclid mở rộng=======================================================
def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, g = egcd(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return (x, y, g)

def modinv(a, m):
    a = a % m  # đảm bảo a không âm
    x, y, g = egcd(a, m)
    if g != 1:
        raise Exception(f"Không tồn tại nghịch đảo modular cho {a} mod {m}")
    return x % m

#======================================================= Use miller-rabin to check prime number=====================================================================
from random import randrange, getrandbits

# 🧪 Kiểm tra nguyên tố bằng Miller-Rabin
def is_prime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Bước 1: phân tích n-1 = 2^s * r (r lẻ)
    s = 0
    r = n - 1
    while r % 2 == 0:
        s += 1
        r //= 2

    # Bước 2: kiểm tra k lần với số ngẫu nhiên a
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)  # tính a^r mod n

        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False  # hợp số
                j += 1
            if x != n - 1:
                return False  # hợp số
    return True  # rất có thể là nguyên tố

# 🎲 Sinh ứng viên số nguyên tố ngẫu nhiên
def generate_prime_candidate(length):
    p = getrandbits(length)         # tạo ngẫu nhiên `length` bit
    p |= (1 << length - 1) | 1      # đảm bảo bit cao nhất = 1 (đủ độ dài) và bit thấp nhất = 1 (số lẻ)
    return p

# 🧮 Sinh số nguyên tố lớn
def generate_prime_number(length=1024):
    p = 4
    while not is_prime(p, 128):     # lặp cho tới khi vượt qua kiểm tra Miller-Rabin
        p = generate_prime_candidate(length)
    return p
#========================================
def prime_factors(n):
    factors = set()
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 1
    if n > 1:
        factors.add(n)
    return list(factors)

def find_primitive_root(p):
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None
#====================================================Eliptic point add and mul===========================================================
def add_points(P, Q, a, p):
    """Cộng hai điểm trên đường cong elliptic"""
    if P == ("O", "O"):
        return Q
    if Q == ("O", "O"):
        return P
    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % p == 0:
        return ("O", "O")

    if P == Q:
        s = ((3 * x1 * x1 + a) * modinv(2 * y1, p)) % p
    else:
        s = ((y2 - y1) * modinv((x2 - x1) % p, p)) % p

    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)

def mul_point(k, P, a, p):
    """Nhân điểm kP"""
    R = ("O", "O")
    for _ in range(k):
        R = add_points(R, P, a, p)
    return R
