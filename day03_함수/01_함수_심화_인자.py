"""
3일차 - 01. 함수 심화 (가변 인자 / 키워드 인자 / 중첩 함수)

2일차에 배운 함수를 더 유연하게 쓰는 방법입니다.
"""

# ---------------------------------------------------------------
# 1. *args - 개수가 정해지지 않은 인자 받기
# ---------------------------------------------------------------

# 인자를 몇 개 받을지 모를 때 매개변수 앞에 * 를 붙입니다.
def total(*numbers):
    """넘어온 값들이 numbers 라는 튜플로 묶입니다."""
    print(f"받은 값: {numbers}, 타입: {type(numbers)}")
    return sum(numbers)


print(total(1, 2))
print(total(1, 2, 3, 4, 5))
print(total())          # 하나도 안 넘겨도 됩니다 → 0

# 이름은 관례적으로 args 를 쓰지만 아무거나 상관없습니다. * 가 핵심입니다.
def print_all(*items):
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")


print_all("사과", "바나나", "포도")


# 리스트를 낱개로 풀어서 넘기려면 호출할 때도 * 를 붙입니다.
scores = [90, 85, 77]
print(total(*scores))      # total(90, 85, 77) 과 같음

# * 를 빼면 리스트 하나가 통째로 들어가 에러가 납니다.
try:
    print(total(scores))
except TypeError as e:
    print(f"* 를 빼면 에러: {e}")


# ---------------------------------------------------------------
# 2. **kwargs - 이름이 붙은 인자를 자유롭게 받기
# ---------------------------------------------------------------

def make_profile(**info):
    """이름=값 형태의 인자들이 info 라는 딕셔너리로 묶입니다."""
    print(f"받은 값: {info}")
    for key, value in info.items():
        print(f"  {key}: {value}")


make_profile(name="김철수", age=20, major="ITM")
make_profile(name="이영희", hobby="독서")

# 딕셔너리를 풀어서 넘기려면 ** 를 붙입니다.
data = {"name": "박민수", "age": 23}
make_profile(**data)


# ---------------------------------------------------------------
# 3. 전부 조합하기
# ---------------------------------------------------------------

# 순서 규칙: 일반 인자 → 기본값 인자 → *args → **kwargs
def order(menu, size="M", *options, **extra):
    print(f"메뉴: {menu}")
    print(f"사이즈: {size}")
    print(f"옵션: {options}")
    print(f"기타: {extra}")


order("아메리카노")
print()
order("라떼", "L", "샷추가", "시럽", ice=True, takeout=False)


# ---------------------------------------------------------------
# 4. 기본값의 함정 - 아주 중요합니다
# ---------------------------------------------------------------

# [잘못된 코드] 기본값에 리스트를 쓰면 함수 전체가 그 하나를 공유합니다.
def add_item_wrong(item, basket=[]):
    basket.append(item)
    return basket


print(add_item_wrong("사과"))     # ['사과']
print(add_item_wrong("바나나"))   # ['사과', '바나나']  ← 앞의 것이 남아 있음!

# [올바른 코드] None 을 기본값으로 두고 함수 안에서 새로 만듭니다.
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket


print(add_item("사과"))     # ['사과']
print(add_item("바나나"))   # ['바나나']  ← 매번 새 리스트


# ---------------------------------------------------------------
# 5. 함수도 값이다 - 변수에 담고 넘길 수 있습니다
# ---------------------------------------------------------------

def double(x):
    return x * 2


f = double            # 괄호를 안 붙이면 '함수 자체'를 가리킵니다
print(f(5))           # 10
print(type(f))        # <class 'function'>


# 함수를 인자로 받는 함수
def apply_twice(func, value):
    """넘겨받은 함수를 두 번 적용합니다."""
    return func(func(value))


print(apply_twice(double, 3))        # 3 → 6 → 12


# 함수를 돌려주는 함수
def make_multiplier(n):
    """n배 해주는 '함수'를 만들어 돌려줍니다."""
    def multiplier(x):
        return x * n
    return multiplier


times3 = make_multiplier(3)
times10 = make_multiplier(10)
print(times3(5))     # 15
print(times10(5))    # 50


# ---------------------------------------------------------------
# 6. 중첩 함수 (함수 안의 함수)
# ---------------------------------------------------------------

def calculate_grade(scores):
    """안쪽 함수는 바깥 함수 안에서만 쓸 수 있습니다."""

    def average(numbers):
        return sum(numbers) / len(numbers)

    def to_grade(value):
        if value >= 90:
            return "A"
        elif value >= 80:
            return "B"
        elif value >= 70:
            return "C"
        return "F"

    avg = average(scores)
    return avg, to_grade(avg)


print(calculate_grade([95, 88, 92]))
# average(...)      ← 함수 밖에서는 부를 수 없습니다 (NameError)


# ---------------------------------------------------------------
# 7. 독스트링(docstring)과 타입 힌트
# ---------------------------------------------------------------

def calculate_discount(price: int, rate: float = 0.1) -> int:
    """할인가를 계산합니다.

    Args:
        price: 정가 (원)
        rate: 할인율 (0.1 이면 10% 할인)

    Returns:
        할인이 적용된 가격 (원 단위, 소수점 버림)
    """
    return int(price * (1 - rate))


print(calculate_discount(10000))         # 9000
print(calculate_discount(10000, 0.3))    # 7000

# 독스트링은 help() 로 볼 수 있습니다.
print(calculate_discount.__doc__)

# 타입 힌트(: int, -> int)는 강제되지 않습니다.
# 사람과 편집기가 읽기 위한 '설명'입니다.


# ---------------------------------------------------------------
# 8. 재귀 함수 - 자기 자신을 부르기
# ---------------------------------------------------------------

def factorial(n):
    """n! 을 재귀로 구합니다."""
    if n <= 1:           # 멈추는 조건(종료 조건)이 반드시 있어야 합니다
        return 1
    return n * factorial(n - 1)


print(factorial(5))      # 120

# 동작 과정
# factorial(5) = 5 * factorial(4)
#              = 5 * 4 * factorial(3)
#              = 5 * 4 * 3 * factorial(2)
#              = 5 * 4 * 3 * 2 * factorial(1)
#              = 5 * 4 * 3 * 2 * 1 = 120


def fibonacci(n):
    """피보나치 수열의 n번째 값"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print([fibonacci(i) for i in range(10)])

# [주의] 종료 조건이 없으면 RecursionError 가 납니다.
# 반복문으로 쓸 수 있으면 반복문이 대체로 더 빠릅니다.


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 여러 개의 점수를 *args 로 받아 평균을 돌려주는 함수를 만드세요.
#    단, 하나도 안 넘어오면 0을 돌려주게 하세요.
#
# 2) **kwargs 로 상품 정보를 받아 "키: 값" 목록을 출력하는 함수를 만드세요.
#
# 3) 함수를 인자로 받아 리스트의 모든 값에 적용하는 함수를 만드세요.
#    apply_all(double, [1,2,3]) → [2,4,6]
#
# 4) 재귀로 리스트의 합을 구하는 함수를 만드세요. (sum 사용 금지)
