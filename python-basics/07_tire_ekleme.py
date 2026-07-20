"""
Görev 7: 

Verilen sayı veya string içerisindeki ardışık iki tek rakamın arasına - karakteri ekleyen bir program yazın.

"""

def insert_dash(value) -> str:
    s = str(value)
    if not s:
        return s

    result = s[0]
    for i in range(1, len(s)):
        prev_char, curr_char = s[i - 1], s[i]
        if prev_char.isdigit() and curr_char.isdigit():
            if int(prev_char) % 2 == 1 and int(curr_char) % 2 == 1:
                result += "-"
        result += curr_char
    return result


if __name__ == "__main__":
    girdi = input("Sayı girin: ")
    print(f"Çıktı: {insert_dash(girdi)}")