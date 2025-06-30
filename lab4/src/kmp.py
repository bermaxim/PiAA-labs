def compute_prefix(pattern: str) -> list[int]:

    length = len(pattern)
    pi = [0] * length
    j = 0
    i = 1
    while i < length:
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
            i += 1
        else:
            if j == 0:
                pi[i] = 0
                i += 1
            else:
                j = pi[j - 1]
    return pi


def kmp(pattern: str, text: str) -> str:

    p_len = len(pattern)
    t_len = len(text)
    pi = compute_prefix(pattern)
    result = []

    i = 0  
    j = 0  

    while i < t_len:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == p_len:
                result.append(i - p_len)
                j = pi[j - 1]
        else:
            if j > 0:
                j = pi[j - 1]
            else:
                i += 1

    return ','.join(map(str, result)) if result else '-1'


if __name__ == '__main__':
    p = input().strip()
    t = input().strip()
    print(kmp(p, t))


