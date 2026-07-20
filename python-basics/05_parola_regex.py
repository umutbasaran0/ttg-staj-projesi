r"""
Görev 5: 
Görev 4'teki doğrulamayı yalnızca tek bir Regular Expression (Regex) kullanarak gerçekleştirin.

regex: buyuk harf + rakam + sembol + "parola" yasagi + 8-30 karakter

"""
import re

PASSWORD_REGEX = re.compile(
    r'^(?!.*(?i:parola))(?=.*[A-Z])(?=.*\d)(?=.*[!-/:-@\[-`{-~]).{8,30}$'
)


def is_valid_password(password: str) -> bool:
    return bool(PASSWORD_REGEX.match(password))


if __name__ == "__main__":
    pwd = input("Parolanızı girin: ")
    if is_valid_password(pwd):
        print("Parola geçerli.")
    else:
        print("Parola geçersiz.")