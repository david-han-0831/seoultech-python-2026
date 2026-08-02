"""
4일차 - 02. 클래스 상속 (Inheritance)

이미 만들어 둔 클래스를 물려받아 확장하는 것입니다.
공통된 부분을 부모 클래스에 두고, 다른 부분만 자식 클래스에 씁니다.
"""

# ---------------------------------------------------------------
# 1. 상속이 없으면 - 중복이 생깁니다
# ---------------------------------------------------------------

class StudentOld:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"{self.name}입니다. {self.age}살입니다.")


class TeacherOld:
    def __init__(self, name, age):     # ← 똑같은 코드
        self.name = name
        self.age = age

    def introduce(self):               # ← 똑같은 코드
        print(f"{self.name}입니다. {self.age}살입니다.")


# ---------------------------------------------------------------
# 2. 상속으로 정리하기
# ---------------------------------------------------------------

class Person:
    """부모 클래스 (상위 클래스, 슈퍼 클래스)"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"안녕하세요, {self.name}입니다. {self.age}살입니다.")

    def birthday(self):
        self.age += 1
        print(f"{self.name}님, 생일 축하합니다! 이제 {self.age}살입니다.")


class Student(Person):        # 괄호 안에 부모 클래스를 씁니다
    """자식 클래스 (하위 클래스, 서브 클래스)"""

    def __init__(self, name, age, student_id, major):
        super().__init__(name, age)     # 부모의 __init__ 을 먼저 실행
        self.student_id = student_id    # 자식만의 속성 추가
        self.major = major

    def study(self):                    # 자식만의 메서드
        print(f"{self.name}이(가) {self.major} 공부를 합니다.")


class Teacher(Person):
    def __init__(self, name, age, subject, salary):
        super().__init__(name, age)
        self.subject = subject
        self.salary = salary

    def teach(self):
        print(f"{self.name} 선생님이 {self.subject}을(를) 가르칩니다.")


# 사용해 보기
s = Student("김철수", 20, "20260001", "ITM")
t = Teacher("한동윤", 35, "파이썬", 5000000)

s.introduce()     # 부모에게 물려받은 메서드
s.study()         # 자기만의 메서드
s.birthday()      # 부모 메서드

t.introduce()
t.teach()

# isinstance 로 확인
print(isinstance(s, Student))   # True
print(isinstance(s, Person))    # True  ← 학생은 사람이기도 합니다
print(isinstance(s, Teacher))   # False


# ---------------------------------------------------------------
# 3. 오버라이딩 - 부모 메서드를 자식이 다시 정의하기
# ---------------------------------------------------------------

class Employee(Person):
    def __init__(self, name, age, company):
        super().__init__(name, age)
        self.company = company

    def introduce(self):
        """같은 이름의 메서드를 새로 만들면 자식 것이 우선합니다."""
        print(f"{self.company}의 {self.name}입니다.")


class Intern(Employee):
    def introduce(self):
        # 부모 것을 먼저 실행하고 내용을 덧붙일 수도 있습니다.
        super().introduce()
        print("  (인턴입니다. 잘 부탁드립니다!)")


print()
Person("일반인", 30).introduce()
Employee("이영희", 28, "콜론비").introduce()
Intern("박민수", 24, "콜론비").introduce()


# ---------------------------------------------------------------
# 4. 다형성 - 같은 이름으로 다르게 동작하기
# ---------------------------------------------------------------

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def describe(self):
        print(f"{self.name}: {self.speak()}")


class Dog(Animal):
    def speak(self):
        return "멍멍!"


class Cat(Animal):
    def speak(self):
        return "야옹~"


class Cow(Animal):
    def speak(self):
        return "음메"


# 하나의 반복문으로 서로 다른 동작을 시킬 수 있습니다.
print()
animals = [Dog("바둑이"), Cat("나비"), Cow("얼룩이"), Animal("무명씨")]
for animal in animals:
    animal.describe()

# 이것이 다형성(polymorphism)입니다.
# '똑같이 speak() 를 부르지만 객체마다 다르게 동작한다'


# ---------------------------------------------------------------
# 5. 실전 예제 - 도형 넓이 계산기
# ---------------------------------------------------------------

class Shape:
    """모든 도형의 부모"""

    def area(self):
        raise NotImplementedError("자식 클래스에서 반드시 구현해야 합니다.")

    def name(self):
        return self.__class__.__name__     # 클래스 이름 문자열

    def __str__(self):
        return f"{self.name()}: 넓이 {self.area():.2f}"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    """정사각형은 가로=세로인 직사각형입니다."""

    def __init__(self, side):
        super().__init__(side, side)


class Circle(Shape):
    PI = 3.141592

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return self.PI * self.radius ** 2


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return self.base * self.height / 2


print("\n[도형 넓이]")
shapes = [Rectangle(3, 4), Square(5), Circle(2), Triangle(6, 3)]

for shape in shapes:
    print(f"  {shape}")

# 넓이 순으로 정렬
print("\n[넓이 큰 순]")
for shape in sorted(shapes, key=lambda s: s.area(), reverse=True):
    print(f"  {shape}")

print(f"\n전체 넓이 합: {sum(s.area() for s in shapes):.2f}")


# ---------------------------------------------------------------
# 6. 캡슐화 - 밖에서 함부로 못 건드리게
# ---------------------------------------------------------------

class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance     # 밑줄 하나: "직접 건드리지 마세요" 라는 약속

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def get_balance(self):
        return self._balance


acc = Account("김철수", 10000)
acc.deposit(5000)
print(f"\n잔액: {acc.get_balance():,}원")

# acc._balance = 999999999   ← 문법적으로는 되지만 하면 안 됩니다


# @property 를 쓰면 메서드를 속성처럼 쓸 수 있습니다.
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("절대영도보다 낮을 수 없습니다.")
        self._celsius = value

    @property
    def fahrenheit(self):
        """계산해서 돌려주지만 쓸 때는 속성처럼 보입니다."""
        return self._celsius * 9 / 5 + 32


t = Temperature(25)
print(f"\n{t.celsius}°C = {t.fahrenheit}°F")   # 괄호 없이 접근

t.celsius = 30
print(f"{t.celsius}°C = {t.fahrenheit}°F")

try:
    t.celsius = -300
except ValueError as e:
    print("에러:", e)


# ===============================================================
# 연습 문제
# ===============================================================
# 1) Vehicle(탈것) 부모 클래스와 Car, Bicycle 자식 클래스를 만드세요.
#    공통: 이름, 바퀴 수 / 각자: 이동 방식 메서드
#
# 2) 4-1의 Product 클래스를 상속해 DiscountProduct 를 만드세요.
#    할인율을 받아 최종 가격을 계산하도록 하세요.
#
# 3) Shape 에 둘레를 구하는 perimeter() 를 추가하고
#    모든 자식 클래스에 구현하세요.
#
# 4) Student 를 상속한 GraduateStudent 를 만들고
#    지도교수 속성과 논문 제출 메서드를 추가하세요.
