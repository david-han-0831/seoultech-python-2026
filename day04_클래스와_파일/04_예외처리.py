"""
4일차 - 04. 예외 처리 (try / except)

프로그램이 에러를 만나면 그 자리에서 멈춰 버립니다.
예외 처리는 '에러가 나도 프로그램이 계속 돌아가게' 만드는 장치입니다.
"""

# ---------------------------------------------------------------
# 1. 예외 처리가 없으면
# ---------------------------------------------------------------

# 아래 주석을 풀면 프로그램이 여기서 죽습니다.
# print(10 / 0)
# print("이 줄은 실행되지 않습니다")


# ---------------------------------------------------------------
# 2. 기본 구조
# ---------------------------------------------------------------

try:
    result = 10 / 0
    print(result)
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")

print("프로그램이 계속 실행됩니다.")


# ---------------------------------------------------------------
# 3. 자주 만나는 예외들
# ---------------------------------------------------------------

# ValueError - 자료형은 맞지만 값이 이상할 때
try:
    int("파이썬")
except ValueError as e:
    print(f"ValueError: {e}")

# TypeError - 자료형이 안 맞을 때
try:
    "문자열" + 10
except TypeError as e:
    print(f"TypeError: {e}")

# IndexError - 리스트 범위를 벗어날 때
try:
    [1, 2, 3][10]
except IndexError as e:
    print(f"IndexError: {e}")

# KeyError - 딕셔너리에 없는 키를 부를 때
try:
    {"a": 1}["b"]
except KeyError as e:
    print(f"KeyError: {e}")

# FileNotFoundError - 없는 파일을 열 때
try:
    open("없는파일.txt")
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")

# ZeroDivisionError
try:
    1 / 0
except ZeroDivisionError as e:
    print(f"ZeroDivisionError: {e}")

# AttributeError - 없는 속성/메서드를 부를 때
try:
    "문자열".없는메서드()
except AttributeError as e:
    print(f"AttributeError: {e}")


# ---------------------------------------------------------------
# 4. 여러 예외를 따로 처리하기
# ---------------------------------------------------------------

def divide(a, b):
    try:
        return int(a) / int(b)
    except ValueError:
        print("  숫자를 입력해 주세요.")
        return None
    except ZeroDivisionError:
        print("  0으로 나눌 수 없습니다.")
        return None


print()
print(divide("10", "2"))      # 5.0
print(divide("십", "2"))       # 숫자 아님
print(divide("10", "0"))      # 0으로 나눔

# 여러 예외를 한 번에 잡기
try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print(f"입력 오류: {e}")


# ---------------------------------------------------------------
# 5. else 와 finally
# ---------------------------------------------------------------

def read_number(text):
    try:
        number = int(text)
    except ValueError:
        print(f"  '{text}' 는 숫자가 아닙니다.")
        return None
    else:
        # 예외가 '안 났을 때만' 실행됩니다.
        print(f"  변환 성공: {number}")
        return number
    finally:
        # 예외가 나든 안 나든 '무조건' 실행됩니다.
        # 파일 닫기, 연결 끊기 등 뒷정리에 씁니다.
        print("  (처리 완료)")


print()
read_number("42")
read_number("abc")


# ---------------------------------------------------------------
# 6. 예외 직접 일으키기 - raise
# ---------------------------------------------------------------

def set_age(age):
    if not isinstance(age, int):
        raise TypeError("나이는 정수여야 합니다.")
    if age < 0:
        raise ValueError("나이는 0 이상이어야 합니다.")
    if age > 150:
        raise ValueError("나이가 너무 큽니다.")
    return age


print()
for value in [25, -5, 200, "스물"]:
    try:
        print(f"  나이 설정: {set_age(value)}")
    except (TypeError, ValueError) as e:
        print(f"  거부됨: {e}")


# ---------------------------------------------------------------
# 7. 나만의 예외 만들기
# ---------------------------------------------------------------

class InsufficientBalanceError(Exception):
    """잔액이 부족할 때 발생하는 예외."""

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"잔액 부족: 잔액 {balance:,}원, 출금 요청 {amount:,}원 "
            f"(부족액 {amount - balance:,}원)"
        )


class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("출금액은 0보다 커야 합니다.")
        if amount > self.balance:
            raise InsufficientBalanceError(self.balance, amount)
        self.balance -= amount
        return self.balance


print()
acc = Account("김철수", 50000)

for amount in [20000, 100000, -1000]:
    try:
        remain = acc.withdraw(amount)
        print(f"  {amount:,}원 출금 성공 (잔액 {remain:,}원)")
    except InsufficientBalanceError as e:
        print(f"  실패: {e}")
        print(f"       (부족액만 따로 꺼낼 수도 있습니다: {e.amount - e.balance:,}원)")
    except ValueError as e:
        print(f"  실패: {e}")


# ---------------------------------------------------------------
# 8. 실전 - 안전한 입력받기
# ---------------------------------------------------------------

def input_int(prompt, min_value=None, max_value=None):
    """정수를 안전하게 입력받습니다. 올바른 값이 들어올 때까지 반복합니다."""
    while True:
        raw = input(prompt).strip()

        try:
            value = int(raw)
        except ValueError:
            print("  숫자를 입력해 주세요.")
            continue

        if min_value is not None and value < min_value:
            print(f"  {min_value} 이상이어야 합니다.")
            continue

        if max_value is not None and value > max_value:
            print(f"  {max_value} 이하여야 합니다.")
            continue

        return value


# 사용 예 (실행하려면 주석을 푸세요)
# score = input_int("점수(0~100): ", min_value=0, max_value=100)
# print(f"입력된 점수: {score}")


# ---------------------------------------------------------------
# 9. 하면 안 되는 예외 처리
# ---------------------------------------------------------------

# [나쁜 예 1] 그냥 다 무시하기 - 무슨 문제가 있는지 영영 모릅니다
# try:
#     중요한작업()
# except:
#     pass

# [나쁜 예 2] 너무 넓게 잡기 - 오타로 인한 에러까지 숨겨 버립니다
# try:
#     result = calcualte()      # 오타인데
# except Exception:
#     result = 0                # 조용히 0이 됩니다

# [좋은 예] 예상되는 예외만 구체적으로 잡고, 무슨 일인지 남깁니다
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("[경고] 0으로 나누려 했습니다. 0을 돌려줍니다.")
        return 0


print()
print(safe_divide(10, 2))
print(safe_divide(10, 0))


# ---------------------------------------------------------------
# 10. 에러 내용 자세히 보기
# ---------------------------------------------------------------

import traceback

try:
    data = {"a": 1}
    print(data["b"])
except KeyError:
    print("\n[상세 에러 정보]")
    traceback.print_exc()      # 어디서 무슨 에러가 났는지 전부 출력


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 두 수를 입력받아 나눗셈하되, 모든 오류 상황을 처리하세요.
#
# 2) 리스트와 인덱스를 받아 값을 돌려주는 함수를 만드세요.
#    범위를 벗어나면 None 을 돌려주게 하세요.
#
# 3) 나이 제한(19세 이상) 예외 클래스를 만들고
#    미성년자가 입장하려 하면 예외를 발생시키세요.
#
# 4) 파일을 읽는 함수를 만들되, 파일이 없으면
#    "파일이 없습니다" 를 출력하고 빈 문자열을 돌려주게 하세요.
