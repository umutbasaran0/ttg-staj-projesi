"""
Görev 3: 
Bir sayının faktöriyelini iki farklı yöntemle hesaplayan program

"""


def factorial_loop(n: int) -> int:  # a.Döngü Kullanarak
    if n < 0:
        raise ValueError("Negatif sayıların faktöriyeli hesaplanamaz.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int: # b.Recursive
    if n < 0:
        raise ValueError("Negatif sayıların faktöriyeli hesaplanamaz.")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


if __name__ == "__main__":
    try:
        num = int(input("Bir sayı girin: "))
        print(f"Döngü ile: {num}! = {factorial_loop(num)}")
        print(f"Recursive ile: {num}! = {factorial_recursive(num)}")
    except ValueError as e:
        print(f"Hata: {e}")