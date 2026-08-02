"""
4일차 - 01. 클래스 기초 (객체 / __init__ / 메서드)

클래스는 '설계도'이고, 객체는 그 설계도로 찍어낸 '실제 물건'입니다.
붕어빵 틀(클래스)로 붕어빵(객체)을 여러 개 만드는 것과 같습니다.
"""

# ---------------------------------------------------------------
# 1. 클래스가 없으면 이렇게 관리합니다
# ---------------------------------------------------------------

# 3일차까지는 딕셔너리로 했습니다.
student1 = {"name": "김철수", "scores": [90, 85, 77]}
student2 = {"name": "이영희", "scores": [88, 92, 95]}


def get_average(student):
    return sum(student["scores"]) / len(student["scores"])


print(get_average(student1))

# 불편한 점
#  - 데이터(딕셔너리)와 기능(함수)이 따로 떨어져 있음
#  - 오타로 없는 키를 써도 실행할 때까지 모름  student["nmae"]
#  - 필수 항목을 빠뜨려도 막을 방법이 없음


# ---------------------------------------------------------------
# 2. 클래스로 묶기
# ---------------------------------------------------------------

class Student:
    """학생 한 명을 표현하는 클래스."""

    def __init__(self, name, scores):
        """객체가 만들어질 때 자동으로 실행됩니다. (생성자)

        self 는 '지금 만들어지는 이 객체' 자신을 가리킵니다.
        """
        self.name = name        # 속성(attribute) 저장
        self.scores = scores

    def average(self):
        """메서드: 클래스 안에 정의된 함수"""
        return sum(self.scores) / len(self.scores)

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        return "F"


# 객체 만들기 (인스턴스 생성)
s1 = Student("김철수", [90, 85, 77])
s2 = Student("이영희", [88, 92, 95])

# 속성 접근
print(s1.name)        # 김철수
print(s1.scores)      # [90, 85, 77]

# 메서드 호출 - 괄호를 붙입니다
print(s1.average())   # 84.0
print(s1.grade())     # B
print(s2.average())

# s1 과 s2 는 서로 다른 객체입니다. 값이 섞이지 않습니다.
s1.name = "김철수(수정)"
print(s1.name, s2.name)


# ---------------------------------------------------------------
# 3. self 이해하기
# ---------------------------------------------------------------

# s1.average() 는 사실 Student.average(s1) 을 부르는 것과 같습니다.
print(Student.average(s1))

# 그래서 메서드의 첫 매개변수는 항상 self 입니다.
# self 를 빼먹으면 에러가 납니다.
#   def average():          ← TypeError
#       return sum(self.scores)


# ---------------------------------------------------------------
# 4. 기본값과 검증을 넣기
# ---------------------------------------------------------------

class Student2:
    def __init__(self, name, scores=None, major="ITM"):
        if not name:
            raise ValueError("이름은 비워 둘 수 없습니다.")

        # 기본값에 리스트를 직접 쓰면 안 되는 이유는 3일차에 배웠습니다.
        self.name = name
        self.scores = scores if scores is not None else []
        self.major = major

    def add_score(self, score):
        """점수를 하나 추가합니다."""
        if not (0 <= score <= 100):
            raise ValueError(f"점수는 0~100 사이여야 합니다. (입력값: {score})")
        self.scores.append(score)

    def average(self):
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)


s = Student2("박민수")
s.add_score(80)
s.add_score(90)
print(f"{s.name} / {s.major} / 평균 {s.average():.1f}")

# 잘못된 값은 막힙니다.
try:
    s.add_score(150)
except ValueError as e:
    print("에러:", e)


# ---------------------------------------------------------------
# 5. __str__ - print() 했을 때 보이는 모습 정하기
# ---------------------------------------------------------------

class Product:
    def __init__(self, name, price, stock=0):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        """print(객체) 할 때 쓰이는 문자열"""
        return f"{self.name} ({self.price:,}원, 재고 {self.stock}개)"

    def __repr__(self):
        """개발자용 표현. 리스트 안에 있을 때 이게 보입니다."""
        return f"Product('{self.name}', {self.price}, {self.stock})"


p = Product("노트북", 1200000, 5)
print(p)          # __str__ 이 쓰임

items = [Product("마우스", 25000), Product("키보드", 89000)]
print(items)      # __repr__ 이 쓰임

# __str__ 이 없으면 <__main__.Product object at 0x...> 같은 게 나옵니다.


# ---------------------------------------------------------------
# 6. 상태를 바꾸는 메서드
# ---------------------------------------------------------------

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        """입금"""
        if amount <= 0:
            print("입금액은 0보다 커야 합니다.")
            return False
        self.balance += amount
        self.history.append(f"입금 +{amount:,}원")
        return True

    def withdraw(self, amount):
        """출금"""
        if amount <= 0:
            print("출금액은 0보다 커야 합니다.")
            return False
        if amount > self.balance:
            print(f"잔액 부족 (잔액 {self.balance:,}원)")
            return False
        self.balance -= amount
        self.history.append(f"출금 -{amount:,}원")
        return True

    def print_history(self):
        print(f"\n[{self.owner}님 거래내역]")
        for record in self.history:
            print(f"  {record}")
        print(f"  현재 잔액: {self.balance:,}원")

    def __str__(self):
        return f"{self.owner}님 계좌 (잔액 {self.balance:,}원)"


account = BankAccount("김철수", 10000)
account.deposit(50000)
account.withdraw(20000)
account.withdraw(1000000)     # 잔액 부족
account.print_history()
print(account)


# ---------------------------------------------------------------
# 7. 클래스 변수 vs 인스턴스 변수
# ---------------------------------------------------------------

class Counter:
    count = 0                 # 클래스 변수: 모든 객체가 함께 씁니다

    def __init__(self, name):
        self.name = name      # 인스턴스 변수: 객체마다 따로
        Counter.count += 1    # 만들어질 때마다 하나씩 증가


a = Counter("A")
b = Counter("B")
c = Counter("C")

print(f"\n만들어진 객체 수: {Counter.count}")   # 3
print(a.name, b.name, c.name)                 # A B C


# ---------------------------------------------------------------
# 8. 딕셔너리 vs 클래스 - 언제 무엇을 쓸까
# ---------------------------------------------------------------
#
# 딕셔너리
#   - 그냥 데이터를 담아 넘길 때
#   - JSON·API 응답처럼 구조가 자주 바뀔 때
#
# 클래스
#   - 데이터와 그 데이터를 다루는 기능이 같이 다닐 때
#   - 같은 모양의 것을 여러 개 만들 때
#   - 값에 규칙(검증)이 필요할 때


# ===============================================================
# 연습 문제
# ===============================================================
# 1) Book 클래스를 만드세요.
#    속성: 제목, 저자, 가격 / 메서드: 할인가 계산, __str__
#
# 2) Rectangle 클래스를 만드세요.
#    속성: 가로, 세로 / 메서드: 넓이, 둘레, 정사각형인지 판별
#
# 3) Timer 클래스를 만드세요.
#    start()/stop() 으로 시간을 재고 elapsed() 로 경과 시간을 돌려주게 하세요.
#    (import time 의 time.time() 을 쓰세요)
#
# 4) 위 BankAccount 에 '이자 붙이기' 메서드를 추가하세요.
