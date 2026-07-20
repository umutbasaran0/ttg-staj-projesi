"""
Görev 6: 
İsim doğrulaması yapan bir regex yazın.

Kurallar:
İsim zorunludur.
Göbek adı opsiyoneldir.
Soyisim zorunludur.
İsim ve göbek adının ilk harfi büyük, kalan harfleri küçük olmalıdır.
Soyisim tamamen büyük harflerden oluşmalıdır.

Not: Türkçe karakterleri de desteklemek için karakter sınıflarına Türkçe harfler eklendi.

"""
import re

UPPER = "A-ZÇĞİÖŞÜ"
LOWER = "a-zçğıöşü"

NAME_REGEX = re.compile(
    rf'^[{UPPER}][{LOWER}]+( [{UPPER}][{LOWER}]+)? [{UPPER}]+$'
)


def is_valid_name(full_name: str) -> bool:
    return bool(NAME_REGEX.match(full_name))


if __name__ == "__main__":
    test_cases = {
        "Cemre MENGU": True,
        "Sude Sevval CILOGLU": True,
        "Cemre Mengu": False,
        "Sude Sevval Ciloglu": False,
        "cemre mengu": False,
        "sude": False,
        "Sude": False,
        "cemre MENGU": False,
    }
    for name, expected in test_cases.items():
        result = is_valid_name(name)
        status = "OK" if result == expected else "HATA"
        print(f"[{status}] '{name}' -> {result} (beklenen: {expected})")