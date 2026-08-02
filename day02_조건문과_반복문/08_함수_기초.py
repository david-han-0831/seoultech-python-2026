"""
2일차 - 08. 함수 기초 (def / return / 매개변수)

함수는 '코드 묶음에 이름을 붙여 재사용하는 것'입니다.
같은 코드를 두 번 이상 쓰게 되면 함수로 만들 때가 된 것입니다.
"""

# ---------------------------------------------------------------
# 1. 함수가 없으면 이렇게 됩니다
# ---------------------------------------------------------------

# 같은 코드가 반복됩니다.
print("=" * 30)
print(" 환영합니다")
print("=" * 30)

print("=" * 30)
print(" 감사합니다")
print("=" * 30)


# ---------------------------------------------------------------
# 2. 함수로 묶기
# ---------------------------------------------------------------

def print_box(message):          # def 함수이름(매개변수):
    """메시지를 선으로 감싸 출력합니다."""
    print("=" * 30)
    print(f" {message}")
    print("=" * 30)


# 만든 함수는 이름으로 '호출'해서 씁니다.
print_box("환영합니다")
print_box("감사합니다")
print_box("아무 말이나 넣어도 됩니다")


# ---------------------------------------------------------------
# 3. 매개변수(parameter)와 인자(argument)
# ---------------------------------------------------------------

def greet(name, age):
    """name, age 는 매개변수입니다."""
    print(f"{name}님은 {age}살입니다.")


greet("김철수", 20)      # "김철수", 20 은 인자입니다
greet("이영희", 22)

# 이름을 지정해 넘기면 순서를 바꿔도 됩니다. (키워드 인자)
greet(age=25, name="박민수")


# ---------------------------------------------------------------
# 4. return - 값을 돌려주기
# ---------------------------------------------------------------

def add(a, b):
    return a + b            # 결과를 '돌려준다'


result = add(3, 5)          # 돌려받은 값을 변수에 담음
print(result)               # 8
print(add(10, 20) * 2)      # 돌려받은 값을 바로 계산에 사용


# print 와 return 은 다릅니다.
def add_print(a, b):
    print(a + b)            # 화면에 보여주기만 함


def add_return(a, b):
    return a + b            # 값을 돌려줌 (다른 곳에서 쓸 수 있음)


x = add_print(1, 2)     # 화면엔 3이 나오지만
print(x)                # x 는 None 입니다!

y = add_return(1, 2)
print(y)                # 3


# return 이 없으면 자동으로 None 을 돌려줍니다.
def no_return():
    pass


print(no_return())      # None


# ---------------------------------------------------------------
# 5. return 은 함수를 즉시 끝냅니다
# ---------------------------------------------------------------

def check_age(age):
    if age < 0:
        return "잘못된 나이입니다"    # 여기서 함수 종료
    if age < 19:
        return "미성년자"
    return "성인"


print(check_age(-5))
print(check_age(15))
print(check_age(30))


# ---------------------------------------------------------------
# 6. 여러 값 돌려주기
# ---------------------------------------------------------------

def min_max_avg(numbers):
    """최솟값, 최댓값, 평균을 한 번에 돌려줍니다."""
    return min(numbers), max(numbers), sum(numbers) / len(numbers)


low, high, avg = min_max_avg([88, 95, 70, 100, 62])
print(f"최소 {low} / 최대 {high} / 평균 {avg:.1f}")

# 통째로 받으면 튜플입니다.
result = min_max_avg([1, 2, 3])
print(result, type(result))


# ---------------------------------------------------------------
# 7. 기본값 매개변수
# ---------------------------------------------------------------

def introduce(name, major="ITM", grade=1):
    """major, grade 는 안 넘기면 기본값이 쓰입니다."""
    print(f"{name} / {major} / {grade}학년")


introduce("김철수")                        # 김철수 / ITM / 1학년
introduce("이영희", "산업공학")              # 이영희 / 산업공학 / 1학년
introduce("박민수", "ITM", 3)              # 박민수 / ITM / 3학년
introduce("최지우", grade=4)                # 중간을 건너뛰려면 이름 지정

# [주의] 기본값이 있는 매개변수는 반드시 뒤에 와야 합니다.
# def wrong(major="ITM", name):   # SyntaxError


# ---------------------------------------------------------------
# 8. 함수 안의 변수는 함수 밖에서 못 씁니다 (지역 변수)
# ---------------------------------------------------------------

def make_message():
    message = "함수 안에서 만든 값"     # 지역 변수
    return message


print(make_message())
# print(message)     # NameError - 함수 밖에서는 존재하지 않습니다


# 밖의 변수를 읽는 것은 됩니다.
school = "서울과기대"


def show_school():
    print(f"학교: {school}")     # 읽기는 가능


show_school()


# 다만 함수 안에서 바꾸려면 global 이 필요합니다. (되도록 피하세요)
counter = 0


def increase():
    global counter
    counter += 1


increase()
increase()
print(counter)      # 2

# 더 나은 방법: 값을 받아서 돌려주기
def increase_better(value):
    return value + 1


counter2 = 0
counter2 = increase_better(counter2)
print(counter2)


# ---------------------------------------------------------------
# 9. 실전 예제 - 지금까지 만든 것을 함수로
# ---------------------------------------------------------------

def get_grade(score):
    """점수를 받아 학점을 돌려줍니다."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


def is_prime(n):
    """소수인지 판별합니다."""
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def bmi(weight, height_m):
    """BMI 를 계산해 (수치, 판정) 을 돌려줍니다."""
    value = weight / (height_m ** 2)
    if value < 18.5:
        status = "저체중"
    elif value < 23:
        status = "정상"
    elif value < 25:
        status = "과체중"
    else:
        status = "비만"
    return value, status


# 사용해 보기
for s in [95, 83, 71, 55]:
    print(f"{s}점 → {get_grade(s)}학점")

print("\n2~30 소수:", [n for n in range(2, 31) if is_prime(n)])

value, status = bmi(68, 1.75)
print(f"\nBMI {value:.1f} → {status}")


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 두 수를 받아 큰 수를 돌려주는 함수를 만드세요. (max 사용 금지)
#
# 2) 문자열을 받아 회문인지 True/False 로 돌려주는 함수를 만드세요.
#
# 3) 리스트를 받아 짝수만 담긴 새 리스트를 돌려주는 함수를 만드세요.
#
# 4) 원의 반지름을 받아 넓이와 둘레를 함께 돌려주는 함수를 만드세요.
#    (원주율은 3.14159 로 계산)
