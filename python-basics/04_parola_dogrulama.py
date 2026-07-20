"""
Görev 4: 
Kullanıcıdan alınan parolanın aşağıdaki kuralları sağlayıp sağlamadığını kontrol edin.

Parola:
En az bir büyük harf içermelidir.
En az bir rakam içermelidir.
En az bir noktalama işareti veya matematiksel sembol içermelidir.
"parola" kelimesini içermemelidir.
Uzunluğu 8 ile 30 karakter arasında olmalıdır.
Program, parolanın geçerli olup olmadığını kullanıcıya bildirmelidir.

"""
import string


def validate_password(password: str) -> list[str]:
    errors = []

    if not (8 <= len(password) <= 30):
        errors.append("Parola 8 ile 30 karakter arasında olmalıdır.")

    if not any(c.isupper() for c in password):
        errors.append("Parola en az bir büyük harf içermelidir.")

    if not any(c.isdigit() for c in password):
        errors.append("Parola en az bir rakam içermelidir.")

    if not any(c in string.punctuation for c in password):
        errors.append("Parola en az bir noktalama işareti veya matematiksel sembol içermelidir.")

    if "parola" in password.lower():
        errors.append("Parola 'parola' kelimesini içeremez.")

    return errors


if __name__ == "__main__":
    pwd = input("Parolanızı girin: ")
    errors = validate_password(pwd)
    if not errors:
        print("Parola geçerli.")
    else:
        print("Parola geçersiz:")
        for e in errors:
            print(f" - {e}")