"""
Görev 2: 
2000 ile 3200 arasındaki;
7'ye tam bölünebilen,
5'in katı olmayan
tüm sayıları bulun ve sonuçları tek satırda, virgülle ayrılmış şekilde yazdırın.

"""

def find_numbers(start=2000, end=3200):
    return [n for n in range(start, end + 1) if n % 7 == 0 and n % 5 != 0]


if __name__ == "__main__":
    numbers = find_numbers()
    print(",".join(str(n) for n in numbers))