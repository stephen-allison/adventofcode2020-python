from itertools import count

SUBJECT_NO = 7
DIVISOR = 20201227
CARD_PUBLIC_KEY = 1965712   # 5764801
DOOR_PUBLIC_KEY = 19072108  # 17807724


def transform(val, subject_no):
    val = val * subject_no
    val = val % DIVISOR
    return val


def find_loop_size(subject_no, public_key):
    val = 1
    for i in count(1):
        val = transform(val, subject_no)
        if val == public_key:
            return i


def encryption_key(key, loop_size):
    val = 1
    for i in range(loop_size):
        val = transform(val, key)
    return val


def solve():
    card_loop_size = find_loop_size(SUBJECT_NO, CARD_PUBLIC_KEY)
    print(f'loop size for {CARD_PUBLIC_KEY} = {card_loop_size}')
    door_loop_size = find_loop_size(SUBJECT_NO, DOOR_PUBLIC_KEY)
    print(f'loop size for {DOOR_PUBLIC_KEY} = {door_loop_size}')

    enc_key = encryption_key(CARD_PUBLIC_KEY, door_loop_size)
    print(f'encryption key = {enc_key}')


if __name__ == '__main__':
    solve()
