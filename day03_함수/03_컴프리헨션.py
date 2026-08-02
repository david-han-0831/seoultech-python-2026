"""
3일차 - 03. 컴프리헨션 (Comprehension)

반복문으로 리스트·딕셔너리를 만드는 일을 한 줄로 줄여 주는 문법입니다.
파이썬 코드를 읽다 보면 아주 자주 나옵니다.
"""

# ---------------------------------------------------------------
# 1. 리스트 컴프리헨션 기본
# ---------------------------------------------------------------

# [기존 방식]
squares = []
for i in range(1, 6):
    squares.append(i ** 2)
print(squares)

# [컴프리헨션]
squares = [i ** 2 for i in range(1, 6)]
print(squares)

# 읽는 순서:  [ 만들 값  for  꺼낼변수  in  목록 ]
#                 ③           ①          ②


# ---------------------------------------------------------------
# 2. 조건 붙이기
# ---------------------------------------------------------------

# 짝수만
evens = [i for i in range(1, 11) if i % 2 == 0]
print(evens)

# 기존 방식과 비교
evens = []
for i in range(1, 11):
    if i % 2 == 0:
        evens.append(i)

# 조건을 두 개 이상
result = [i for i in range(1, 51) if i % 3 == 0 if i % 5 == 0]
print(result)     # 15, 30, 45

# and 로 써도 같습니다
result = [i for i in range(1, 51) if i % 3 == 0 and i % 5 == 0]
print(result)


# ---------------------------------------------------------------
# 3. if-else 는 앞쪽에 씁니다 - 헷갈리는 부분
# ---------------------------------------------------------------

numbers = [1, 2, 3, 4, 5, 6]

# 조건에 맞는 것만 '고를' 때 → for 뒤에 if
picked = [n for n in numbers if n % 2 == 0]
print(picked)      # [2, 4, 6]

# 모든 값을 '변환'하되 조건에 따라 다르게 → for 앞에 if-else
labeled = ["짝수" if n % 2 == 0 else "홀수" for n in numbers]
print(labeled)     # ['홀수', '짝수', '홀수', '짝수', '홀수', '짝수']

# 둘 다 쓰기 (3의 배수만 골라서, 그중 짝수는 다르게 표시)
mixed = ["큰값" if n > 3 else "작은값" for n in numbers if n % 3 == 0]
print(mixed)       # ['작은값', '큰값']


# ---------------------------------------------------------------
# 4. 문자열 다루기
# ---------------------------------------------------------------

words = ["python", "java", "go", "javascript"]

print([w.upper() for w in words])
print([len(w) for w in words])
print([w for w in words if len(w) > 4])
print([w[0].upper() + w[1:] for w in words])     # 첫 글자만 대문자

sentence = "Python is really awesome"
print([w for w in sentence.split() if len(w) > 2])

# 문자열에서 숫자만 뽑기
text = "a1b2c3d4"
print([c for c in text if c.isdigit()])          # ['1','2','3','4']
print("".join([c for c in text if c.isdigit()])) # '1234'


# ---------------------------------------------------------------
# 5. 중첩 컴프리헨션
# ---------------------------------------------------------------

# 2차원 리스트 만들기 (2일차에 봤던 올바른 방법)
grid = [[0] * 3 for _ in range(3)]
print(grid)

# 구구단 표
table = [[dan * i for i in range(1, 10)] for dan in range(2, 5)]
for row in table:
    print(row)

# 2차원을 1차원으로 펴기 (flatten)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [value for row in matrix for value in row]
print(flat)     # [1,2,3,4,5,6,7,8,9]

# 순서 주의: 바깥 for 를 먼저 씁니다. 아래 중첩 반복문과 순서가 같습니다.
#   for row in matrix:
#       for value in row:

# 조합 만들기
sizes = ["S", "M", "L"]
colors = ["빨강", "파랑"]
combos = [f"{c} {s}" for c in colors for s in sizes]
print(combos)


# ---------------------------------------------------------------
# 6. 딕셔너리 컴프리헨션
# ---------------------------------------------------------------

# {키: 값 for ...}
squares_dict = {i: i ** 2 for i in range(1, 6)}
print(squares_dict)     # {1:1, 2:4, 3:9, 4:16, 5:25}

# 두 리스트를 딕셔너리로
names = ["김철수", "이영희", "박민수"]
scores = [88, 95, 70]
score_map = {n: s for n, s in zip(names, scores)}
print(score_map)

# dict(zip(...)) 로도 됩니다
print(dict(zip(names, scores)))

# 키와 값 뒤집기
reversed_map = {v: k for k, v in score_map.items()}
print(reversed_map)

# 조건 붙이기 - 80점 이상만
passed = {n: s for n, s in score_map.items() if s >= 80}
print(passed)

# 값 가공하기 - 모든 점수에 5점 가산 (100점 초과 방지)
curved = {n: min(s + 5, 100) for n, s in score_map.items()}
print(curved)


# ---------------------------------------------------------------
# 7. 집합 컴프리헨션
# ---------------------------------------------------------------

text = "hello world"
unique_chars = {c for c in text if c != " "}
print(unique_chars)     # 중복 없는 글자들

# 리스트의 중복 제거 + 가공
numbers = [1, 2, 2, 3, 3, 3]
print({n ** 2 for n in numbers})     # {1, 4, 9}


# ---------------------------------------------------------------
# 8. 제너레이터 표현식 - 메모리를 아끼는 방법
# ---------------------------------------------------------------

# 대괄호 대신 소괄호를 쓰면 '한 번에 하나씩 만들어 내는' 제너레이터가 됩니다.
gen = (i ** 2 for i in range(1000000))
print(type(gen))     # <class 'generator'>

# 리스트는 100만 개를 전부 메모리에 올리지만, 제너레이터는 그렇지 않습니다.
# sum, max 같은 함수에 넘길 때는 대괄호를 뺄 수 있습니다.
print(sum(i ** 2 for i in range(1, 101)))

# 조건에 맞는 개수 세기 (자주 쓰는 관용구)
scores = [88, 95, 70, 100, 62]
print(sum(1 for s in scores if s >= 80))     # 3


# ---------------------------------------------------------------
# 9. 언제 쓰고 언제 쓰지 말아야 할까
# ---------------------------------------------------------------

# [좋은 예] 한눈에 읽히는 짧은 변환
names = ["kim", "lee"]
upper = [n.upper() for n in names]

# [나쁜 예] 너무 길고 복잡함
bad = [x * 2 if x % 2 == 0 else x * 3 for sub in [[1, 2], [3, 4]] for x in sub if x > 1]

# 이럴 땐 그냥 for 문으로 풀어 쓰는 게 낫습니다.
good = []
for sub in [[1, 2], [3, 4]]:
    for x in sub:
        if x <= 1:
            continue
        good.append(x * 2 if x % 2 == 0 else x * 3)

print(bad == good)     # True - 결과는 같지만 아래가 읽기 쉽습니다

# 기준: 한 줄에 for 가 두 개를 넘거나, 세로로 두 줄이 넘어가면
#       for 문으로 풀어 쓰는 것을 고려하세요.


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 1~100 중 4의 배수이면서 6의 배수인 수를 컴프리헨션으로 구하세요.
#
# 2) 문자열 리스트에서 'a' 가 들어간 단어만 대문자로 바꿔 리스트를 만드세요.
#
# 3) 아래 데이터를 {이름: 평균점수} 딕셔너리로 만드세요.
#    data = [("김철수",[90,80]), ("이영희",[95,85])]
#
# 4) 3x3 행렬의 전치행렬을 컴프리헨션으로 만드세요.
