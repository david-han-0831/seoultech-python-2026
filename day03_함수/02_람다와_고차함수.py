"""
3일차 - 02. 람다(lambda)와 고차 함수

람다는 '이름 없는 한 줄짜리 함수'입니다.
정렬 기준을 알려줄 때처럼, 함수를 잠깐 쓰고 버릴 때 유용합니다.
"""

# ---------------------------------------------------------------
# 1. 람다 기본
# ---------------------------------------------------------------

# 일반 함수
def double(x):
    return x * 2


# 같은 일을 하는 람다
double_lambda = lambda x: x * 2

print(double(5))
print(double_lambda(5))

# 문법:  lambda 매개변수: 돌려줄값
#  - def 와 달리 return 을 쓰지 않습니다 (자동으로 돌려줌)
#  - 한 줄만 쓸 수 있습니다

add = lambda a, b: a + b
print(add(3, 4))

is_even = lambda n: n % 2 == 0
print(is_even(10))     # True

# 조건도 넣을 수 있습니다 (삼항 연산자)
grade = lambda s: "합격" if s >= 60 else "불합격"
print(grade(75))


# ---------------------------------------------------------------
# 2. 람다를 쓰는 진짜 이유 - 정렬 기준 지정
# ---------------------------------------------------------------

students = [
    {"name": "김철수", "score": 88, "age": 21},
    {"name": "이영희", "score": 95, "age": 20},
    {"name": "박민수", "score": 70, "age": 23},
    {"name": "최지우", "score": 95, "age": 22},
]

# 점수 순 정렬
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
for s in by_score:
    print(f"{s['name']}: {s['score']}점")

# 이름 가나다순
by_name = sorted(students, key=lambda s: s["name"])
print([s["name"] for s in by_name])

# 여러 기준으로 정렬 (점수 내림차순 → 같으면 나이 오름차순)
# 튜플로 넘기면 앞에서부터 순서대로 비교합니다.
by_multi = sorted(students, key=lambda s: (-s["score"], s["age"]))
print("\n[점수 높은 순, 같으면 어린 순]")
for s in by_multi:
    print(f"  {s['name']} {s['score']}점 {s['age']}세")

# 문자열 길이순 정렬
words = ["python", "is", "awesome", "language"]
print(sorted(words, key=lambda w: len(w)))
print(sorted(words, key=len))     # 함수 이름만 넘겨도 됩니다

# max / min 에도 똑같이 씁니다
print(max(students, key=lambda s: s["score"])["name"])


# ---------------------------------------------------------------
# 3. map - 모든 값에 함수 적용하기
# ---------------------------------------------------------------

numbers = [1, 2, 3, 4, 5]

# map(함수, 목록) → 각 값에 함수를 적용한 결과
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)     # [2, 4, 6, 8, 10]

# 문자열을 숫자로 (2일차에 입력받을 때 이미 썼습니다)
str_numbers = ["10", "20", "30"]
print(list(map(int, str_numbers)))

# 대문자로
names = ["kim", "lee", "park"]
print(list(map(str.upper, names)))

# 컴프리헨션으로도 같은 일을 할 수 있습니다. 보통 이쪽이 더 읽기 쉽습니다.
print([x * 2 for x in numbers])


# ---------------------------------------------------------------
# 4. filter - 조건에 맞는 것만 걸러내기
# ---------------------------------------------------------------

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)      # [2, 4, 6, 8, 10]

# 컴프리헨션 버전
print([x for x in numbers if x % 2 == 0])

# 딕셔너리 목록 거르기
passed = list(filter(lambda s: s["score"] >= 80, students))
print([s["name"] for s in passed])

# 빈 문자열 제거
words = ["python", "", "java", "", "go"]
print(list(filter(None, words)))     # None 을 넘기면 '참인 값만' 남깁니다


# ---------------------------------------------------------------
# 5. 정렬·필터를 조합한 실전 예제
# ---------------------------------------------------------------

products = [
    {"name": "노트북", "price": 1200000, "stock": 5},
    {"name": "마우스", "price": 25000, "stock": 30},
    {"name": "키보드", "price": 89000, "stock": 0},
    {"name": "모니터", "price": 350000, "stock": 12},
    {"name": "웹캠", "price": 45000, "stock": 3},
]

# 재고가 있는 상품만, 가격 낮은 순
available = sorted(
    [p for p in products if p["stock"] > 0],
    key=lambda p: p["price"],
)

print("\n[구매 가능 상품 - 가격순]")
for p in available:
    print(f"  {p['name']:<8} {p['price']:>10,}원  (재고 {p['stock']}개)")

# 총 재고 금액
total_value = sum(p["price"] * p["stock"] for p in products)
print(f"\n총 재고 금액: {total_value:,}원")

# 재고 부족(5개 이하) 상품 이름만
low_stock = [p["name"] for p in products if 0 < p["stock"] <= 5]
print(f"재고 부족: {', '.join(low_stock)}")

# 품절 상품
sold_out = [p["name"] for p in products if p["stock"] == 0]
print(f"품절: {', '.join(sold_out)}")


# ---------------------------------------------------------------
# 6. 람다를 쓰지 말아야 할 때
# ---------------------------------------------------------------

# [나쁜 예] 복잡한 로직을 람다에 욱여넣기
bad = lambda s: "A" if s >= 90 else ("B" if s >= 80 else ("C" if s >= 70 else "F"))

# [좋은 예] 이럴 땐 그냥 def 로 만드세요. 이름도 있고 읽기도 쉽습니다.
def to_grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"


print(to_grade(85))

# 정리
#  - 람다: 한 줄로 끝나는 간단한 기준(정렬 key 등)
#  - def : 그 외 전부. 재사용하거나 설명이 필요하면 무조건 def


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 리스트 [3, -1, 4, -5, 9] 를 절댓값 기준으로 정렬하세요.
#
# 2) 아래 데이터를 '이름 길이 → 같으면 가나다순' 으로 정렬하세요.
#    names = ["김철수", "이영희정", "박민수", "최지우", "정하늘별"]
#
# 3) filter 와 map 을 함께 써서
#    1~20 중 3의 배수만 골라 제곱한 리스트를 만드세요.
#
# 4) 상품 목록에서 '가격 대비 재고가 가장 많은' 상품을 찾으세요.
