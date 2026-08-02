"""
3일차 - 04. 중첩 자료구조 탐색

실무 데이터(API 응답, JSON, DB 결과)는
'리스트 안에 딕셔너리, 그 안에 또 리스트' 처럼 겹겹이 쌓여 있습니다.
이걸 자유롭게 파고드는 연습을 합니다.
"""

# ---------------------------------------------------------------
# 1. 리스트 안의 딕셔너리 (가장 흔한 모양)
# ---------------------------------------------------------------

students = [
    {"name": "김철수", "major": "ITM", "scores": [90, 85, 77]},
    {"name": "이영희", "major": "ITM", "scores": [88, 92, 95]},
    {"name": "박민수", "major": "산업공학", "scores": [70, 65, 80]},
    {"name": "최지우", "major": "ITM", "scores": [100, 98, 96]},
    {"name": "정하늘", "major": "산업공학", "scores": [55, 60, 72]},
]

# 한 겹씩 들어가 보기
print(students[0])                 # 딕셔너리 하나
print(students[0]["name"])         # 김철수
print(students[0]["scores"])       # [90, 85, 77]
print(students[0]["scores"][0])    # 90

# 전체 순회
for s in students:
    avg = sum(s["scores"]) / len(s["scores"])
    print(f"{s['name']:<8} {s['major']:<8} 평균 {avg:.1f}")


# ---------------------------------------------------------------
# 2. 필터링 - 조건에 맞는 것만 뽑기
# ---------------------------------------------------------------

# ITM 전공만
itm = [s for s in students if s["major"] == "ITM"]
print(f"\nITM 전공: {[s['name'] for s in itm]}")

# 평균 80점 이상
high = [s for s in students if sum(s["scores"]) / len(s["scores"]) >= 80]
print(f"평균 80 이상: {[s['name'] for s in high]}")

# 모든 과목이 70점 이상인 학생 (all 사용)
solid = [s for s in students if all(score >= 70 for score in s["scores"])]
print(f"전 과목 70점 이상: {[s['name'] for s in solid]}")

# 한 과목이라도 90점 이상인 학생 (any 사용)
has_90 = [s for s in students if any(score >= 90 for score in s["scores"])]
print(f"90점 이상 과목 보유: {[s['name'] for s in has_90]}")


# ---------------------------------------------------------------
# 3. 그룹으로 묶기 - 전공별로 나누기
# ---------------------------------------------------------------

by_major = {}
for s in students:
    major = s["major"]
    if major not in by_major:
        by_major[major] = []      # 처음 보는 전공이면 빈 리스트를 만들어 둠
    by_major[major].append(s["name"])

print("\n[전공별 학생]")
for major, names in by_major.items():
    print(f"  {major}: {', '.join(names)} ({len(names)}명)")

# setdefault 를 쓰면 if 를 없앨 수 있습니다.
by_major2 = {}
for s in students:
    by_major2.setdefault(s["major"], []).append(s["name"])
print(by_major2)

# defaultdict 를 쓰면 더 깔끔합니다.
from collections import defaultdict

by_major3 = defaultdict(list)
for s in students:
    by_major3[s["major"]].append(s["name"])
print(dict(by_major3))


# ---------------------------------------------------------------
# 4. 딕셔너리 안의 딕셔너리
# ---------------------------------------------------------------

departments = {
    "ITM": {
        "professor": "홍길동",
        "students": 40,
        "courses": {
            "파이썬": {"credit": 3, "semester": 1},
            "데이터베이스": {"credit": 3, "semester": 2},
        },
    },
    "산업공학": {
        "professor": "김영수",
        "students": 55,
        "courses": {
            "통계학": {"credit": 3, "semester": 1},
            "최적화": {"credit": 2, "semester": 2},
        },
    },
}

# 깊이 들어가기
print(departments["ITM"]["courses"]["파이썬"]["credit"])     # 3

# 전체 훑기
print("\n[학과 정보]")
for dept_name, dept in departments.items():
    print(f"\n{dept_name} (교수: {dept['professor']}, 학생 {dept['students']}명)")
    for course_name, course in dept["courses"].items():
        print(f"  - {course_name}: {course['credit']}학점, {course['semester']}학기")

# 전체 학점 합
total_credit = 0
for dept in departments.values():
    for course in dept["courses"].values():
        total_credit += course["credit"]
print(f"\n전체 학점: {total_credit}")

# 컴프리헨션 한 줄로
total_credit = sum(
    c["credit"]
    for dept in departments.values()
    for c in dept["courses"].values()
)
print(f"전체 학점(컴프리헨션): {total_credit}")


# ---------------------------------------------------------------
# 5. 없는 키 때문에 죽지 않게 - 안전한 탐색
# ---------------------------------------------------------------

data = {"user": {"profile": {"name": "김철수"}}}

# 위험한 방법
print(data["user"]["profile"]["name"])
# print(data["user"]["settings"]["theme"])   # KeyError!

# 안전한 방법 1: get 을 이어 쓰기
theme = data.get("user", {}).get("settings", {}).get("theme", "기본값")
print(theme)     # 기본값

# 안전한 방법 2: 함수로 만들어 두기
def deep_get(dictionary, keys, default=None):
    """keys 를 순서대로 따라 들어가며 값을 찾습니다."""
    current = dictionary
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


print(deep_get(data, ["user", "profile", "name"]))         # 김철수
print(deep_get(data, ["user", "settings", "theme"], "다크"))  # 다크


# ---------------------------------------------------------------
# 6. 실전 - API 응답처럼 생긴 데이터 다루기
# ---------------------------------------------------------------

# 5일차에 배울 API 응답이 대체로 이런 모양입니다.
response = {
    "status": "OK",
    "totalCount": 3,
    "items": [
        {
            "stationName": "종로구",
            "dataTime": "2026-08-03 13:00",
            "pm10Value": "45",
            "pm25Value": "23",
        },
        {
            "stationName": "강남구",
            "dataTime": "2026-08-03 13:00",
            "pm10Value": "82",
            "pm25Value": "41",
        },
        {
            "stationName": "노원구",
            "dataTime": "2026-08-03 13:00",
            "pm10Value": "-",       # 측정값이 없는 경우도 있습니다
            "pm25Value": "18",
        },
    ],
}


def grade_pm10(value):
    """미세먼지 등급을 판정합니다."""
    if value <= 30:
        return "좋음"
    elif value <= 80:
        return "보통"
    elif value <= 150:
        return "나쁨"
    return "매우나쁨"


print("\n[미세먼지 현황]")
print(f"조회 결과: {response['totalCount']}건\n")

valid_values = []

for item in response["items"]:
    station = item["stationName"]
    raw = item["pm10Value"]

    # 실무 데이터는 항상 지저분합니다. 방어 코드가 필요합니다.
    if not raw.isdigit():
        print(f"  {station:<8} 측정값 없음")
        continue

    pm10 = int(raw)
    valid_values.append(pm10)
    print(f"  {station:<8} PM10 {pm10:>3}㎍/㎥  →  {grade_pm10(pm10)}")

if valid_values:
    print(f"\n평균 PM10: {sum(valid_values) / len(valid_values):.1f}㎍/㎥")
    print(f"최고 지역 PM10: {max(valid_values)}㎍/㎥")


# ===============================================================
# 연습 문제
# ===============================================================
# 1) students 데이터에서 과목별(1·2·3번째 과목) 평균을 구하세요.
#
# 2) 전공별 평균 점수를 구해 높은 순으로 출력하세요.
#
# 3) 아래 주문 데이터에서 총 매출과 상품별 판매 수량을 구하세요.
#    orders = [
#        {"id":1, "items":[{"name":"커피","qty":2,"price":4500},
#                          {"name":"케이크","qty":1,"price":6000}]},
#        {"id":2, "items":[{"name":"커피","qty":1,"price":4500}]},
#    ]
#
# 4) departments 에서 1학기 과목만 골라 학과와 함께 출력하세요.
