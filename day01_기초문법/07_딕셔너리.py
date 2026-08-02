"""
1일차 - 07. 딕셔너리 (Dictionary)

리스트가 '번호'로 값을 꺼낸다면, 딕셔너리는 '이름(키)'으로 값을 꺼냅니다.
실무 데이터(JSON, API 응답, DB 조회 결과)는 대부분 이 모양입니다.
"""

# ---------------------------------------------------------------
# 1. 딕셔너리 만들기 - {키: 값}
# ---------------------------------------------------------------

student = {
    "name": "김철수",
    "age": 20,
    "major": "ITM",
    "scores": [90, 85, 77],   # 값에는 어떤 자료형이든 넣을 수 있습니다
}

print(student)
print(len(student))  # 4   키의 개수

empty = {}           # 빈 딕셔너리


# ---------------------------------------------------------------
# 2. 값 꺼내기
# ---------------------------------------------------------------

print(student["name"])    # 김철수
print(student["scores"])  # [90, 85, 77]
print(student["scores"][0])  # 90   중첩된 값도 이어서 접근

# 없는 키를 부르면 에러가 납니다.
# print(student["phone"])   # KeyError

# get() 은 없어도 에러 없이 None 을 돌려줍니다.
print(student.get("phone"))            # None
print(student.get("phone", "없음"))     # 없음   ← 기본값 지정 가능

# 키가 있는지 먼저 확인하는 방법
if "phone" in student:
    print(student["phone"])
else:
    print("전화번호가 등록되어 있지 않습니다.")


# ---------------------------------------------------------------
# 3. 값 추가·수정·삭제
# ---------------------------------------------------------------

student["phone"] = "010-1234-5678"   # 없는 키 → 추가
student["age"] = 21                  # 있는 키 → 수정
print(student)

del student["phone"]                 # 삭제
print(student)

removed = student.pop("major")       # 꺼내면서 삭제
print(removed, student)

student.update({"grade": 3, "age": 22})  # 여러 개 한 번에 추가/수정
print(student)


# ---------------------------------------------------------------
# 4. 순회하기 - keys / values / items
# ---------------------------------------------------------------

person = {"이름": "이영희", "나이": 22, "전공": "ITM"}

print(list(person.keys()))    # ['이름', '나이', '전공']
print(list(person.values()))  # ['이영희', 22, 'ITM']
print(list(person.items()))   # [('이름', '이영희'), ...]  튜플의 리스트

# 키만 필요할 때 (그냥 for x in 딕셔너리 하면 키가 나옵니다)
for key in person:
    print(key, end=" ")
print()

# 값만 필요할 때
for value in person.values():
    print(value, end=" ")
print()

# 키와 값 둘 다 필요할 때 → items()  (가장 많이 씁니다)
for key, value in person.items():
    print(f"{key}: {value}")


# ---------------------------------------------------------------
# 5. 실전 패턴 1 - 개수 세기
# ---------------------------------------------------------------

text = "banana"
counter = {}

for char in text:
    if char in counter:
        counter[char] += 1
    else:
        counter[char] = 1

print(counter)   # {'b': 1, 'a': 3, 'n': 2}

# get() 을 쓰면 if 없이 한 줄로 됩니다. 자주 쓰는 관용구입니다.
counter2 = {}
for char in text:
    counter2[char] = counter2.get(char, 0) + 1
print(counter2)

# 표준 라이브러리를 쓰면 더 짧습니다. (3일차에서 다룹니다)
from collections import Counter
print(Counter(text))


# ---------------------------------------------------------------
# 6. 실전 패턴 2 - 딕셔너리를 담은 리스트 (가장 흔한 데이터 모양)
# ---------------------------------------------------------------

students = [
    {"name": "김철수", "score": 90},
    {"name": "이영희", "score": 85},
    {"name": "박민수", "score": 77},
    {"name": "최지우", "score": 95},
]

# 전체 출력
for s in students:
    print(f"{s['name']}: {s['score']}점")

# 평균 구하기
total = 0
for s in students:
    total += s["score"]
print(f"평균: {total / len(students):.1f}점")

# 80점 이상만 뽑기
passed = []
for s in students:
    if s["score"] >= 80:
        passed.append(s["name"])
print("80점 이상:", passed)

# 점수 순으로 정렬 (key 에 '무엇을 기준으로 정렬할지' 알려줍니다)
ranked = sorted(students, key=lambda s: s["score"], reverse=True)
for i, s in enumerate(ranked, start=1):
    print(f"{i}등: {s['name']} ({s['score']}점)")

# 최고점 학생 찾기
top = max(students, key=lambda s: s["score"])
print("1등:", top["name"])


# ---------------------------------------------------------------
# 7. 중첩 딕셔너리
# ---------------------------------------------------------------

school = {
    "ITM": {
        "교수": "홍길동",
        "학생수": 40,
        "과목": ["파이썬", "데이터베이스"],
    },
    "산업공학": {
        "교수": "김영수",
        "학생수": 55,
        "과목": ["통계", "최적화"],
    },
}

print(school["ITM"]["교수"])        # 홍길동
print(school["ITM"]["과목"][0])     # 파이썬

for dept, info in school.items():
    print(f"[{dept}] 교수 {info['교수']} / 학생 {info['학생수']}명")
    for subject in info["과목"]:
        print(f"  - {subject}")


# ---------------------------------------------------------------
# 8. 키로 쓸 수 있는 것 / 없는 것
# ---------------------------------------------------------------

ok = {
    1: "숫자 가능",
    "a": "문자열 가능",
    (1, 2): "튜플 가능",
}
# 리스트는 키가 될 수 없습니다. (내용이 바뀔 수 있어서)
# bad = {[1, 2]: "불가능"}   # TypeError


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 본인의 정보(이름, 학번, 전공, 취미 목록)를 딕셔너리로 만들고
#    "키: 값" 형태로 한 줄씩 출력하세요.
#
# 2) 아래 데이터에서 재고가 10개 미만인 상품 이름만 출력하세요.
#    products = [
#        {"name": "노트북", "stock": 5},
#        {"name": "마우스", "stock": 30},
#        {"name": "키보드", "stock": 8},
#    ]
#
# 3) 문장을 입력받아 각 단어가 몇 번 나왔는지 딕셔너리로 세어 보세요.
#
# 4) 학생 이름을 키로, 점수 리스트를 값으로 하는 딕셔너리를 만들고
#    학생별 평균 점수를 출력하세요.
