"""
4일차 - 07. JSON 다루기

JSON 은 데이터를 주고받는 표준 형식입니다.
5일차에 배울 API 는 거의 전부 JSON 으로 응답합니다.
생김새가 파이썬 딕셔너리와 거의 같아서 다루기 쉽습니다.
"""

import json
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------
# 1. JSON 은 이렇게 생겼습니다
# ---------------------------------------------------------------

json_text = """
{
    "name": "김철수",
    "age": 20,
    "major": "ITM",
    "is_enrolled": true,
    "scores": [90, 85, 77],
    "address": {
        "city": "서울",
        "district": "노원구"
    },
    "advisor": null
}
"""

# 파이썬 딕셔너리와 다른 점
#   true  / false  →  파이썬은 True / False
#   null           →  파이썬은 None
#   키는 반드시 큰따옴표 (작은따옴표 안 됨)
#   마지막 항목 뒤에 쉼표를 붙이면 에러


# ---------------------------------------------------------------
# 2. 문자열 ↔ 파이썬 객체 변환
# ---------------------------------------------------------------

# loads : 문자열(string) → 파이썬  ('s' 는 string 의 s)
data = json.loads(json_text)
print(type(data))          # <class 'dict'>
print(data["name"])        # 김철수
print(data["scores"])      # [90, 85, 77]
print(data["address"]["city"])   # 서울
print(data["is_enrolled"])       # True   ← true 가 True 로 바뀜
print(data["advisor"])           # None   ← null 이 None 으로 바뀜

# dumps : 파이썬 → 문자열
text = json.dumps(data)
print(f"\n{text}")

# 한글이 \uXXXX 로 깨져 보이면 ensure_ascii=False 를 붙이세요.
text = json.dumps(data, ensure_ascii=False)
print(f"\n{text}")

# 보기 좋게 들여쓰기
text = json.dumps(data, ensure_ascii=False, indent=2)
print(f"\n{text}")


# ---------------------------------------------------------------
# 3. 파일로 저장하고 읽기
# ---------------------------------------------------------------

path = os.path.join(OUTPUT_DIR, "student.json")

students = [
    {"name": "김철수", "major": "ITM", "scores": [90, 85, 77]},
    {"name": "이영희", "major": "ITM", "scores": [88, 92, 95]},
    {"name": "박민수", "major": "산업공학", "scores": [70, 65, 80]},
]

# dump : 파일에 쓰기 (s 가 없습니다)
with open(path, "w", encoding="utf-8") as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

print(f"\n'{path}' 저장 완료")

# load : 파일에서 읽기
with open(path, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(f"불러온 학생 수: {len(loaded)}명")
for s in loaded:
    avg = sum(s["scores"]) / len(s["scores"])
    print(f"  {s['name']}: 평균 {avg:.1f}")

# 정리
#   json.loads() / json.dumps()  →  문자열 상대
#   json.load()  / json.dump()   →  파일 상대


# ---------------------------------------------------------------
# 4. CSV 와 비교
# ---------------------------------------------------------------
#
#  CSV                          JSON
#  --------------------------   --------------------------
#  표 형태만 가능                중첩 구조 가능
#  값은 전부 문자열              자료형 유지 (숫자·불리언·null)
#  엑셀에서 바로 열림            사람이 읽기 좋음
#  용량이 작음                   용량이 큼
#  → 통계 데이터, 엑셀 연동      → 설정 파일, API 통신


# ---------------------------------------------------------------
# 5. 실전 - 설정 파일 만들기
# ---------------------------------------------------------------

CONFIG_PATH = os.path.join(OUTPUT_DIR, "config.json")

DEFAULT_CONFIG = {
    "app_name": "성적 관리 프로그램",
    "version": "1.0",
    "settings": {
        "theme": "light",
        "auto_save": True,
        "max_students": 100,
    },
    "subjects": ["국어", "영어", "수학"],
}


def load_config():
    """설정을 읽습니다. 없거나 깨졌으면 기본값을 씁니다."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  설정 파일이 없어 기본값으로 새로 만듭니다.")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    except json.JSONDecodeError as e:
        # 파일이 깨져 있을 때 (쉼표 누락 등)
        print(f"  설정 파일이 손상되었습니다: {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


print("\n[설정 파일]")
config = load_config()
print(f"  앱 이름: {config['app_name']}")
print(f"  테마: {config['settings']['theme']}")

# 설정 바꾸고 저장
config["settings"]["theme"] = "dark"
save_config(config)
print(f"  변경 후 테마: {load_config()['settings']['theme']}")


# ---------------------------------------------------------------
# 6. 클래스 객체를 JSON 으로 저장하기
# ---------------------------------------------------------------

class Student:
    def __init__(self, name, major, scores):
        self.name = name
        self.major = major
        self.scores = scores

    def to_dict(self):
        """JSON 으로 저장할 수 있게 딕셔너리로 바꿉니다."""
        return {"name": self.name, "major": self.major, "scores": self.scores}

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 객체를 다시 만듭니다."""
        return cls(data["name"], data["major"], data["scores"])

    def __str__(self):
        avg = sum(self.scores) / len(self.scores)
        return f"{self.name}({self.major}) 평균 {avg:.1f}"


objects = [
    Student("김철수", "ITM", [90, 85, 77]),
    Student("이영희", "ITM", [88, 92, 95]),
]

obj_path = os.path.join(OUTPUT_DIR, "objects.json")

# 저장 : 객체 → 딕셔너리 → JSON
with open(obj_path, "w", encoding="utf-8") as f:
    json.dump([s.to_dict() for s in objects], f, ensure_ascii=False, indent=2)

# 불러오기 : JSON → 딕셔너리 → 객체
with open(obj_path, "r", encoding="utf-8") as f:
    restored = [Student.from_dict(d) for d in json.load(f)]

print("\n[객체 저장/복원]")
for s in restored:
    print(f"  {s}")

# json.dump(objects) 는 에러입니다.
# JSON 은 클래스 객체를 모릅니다. 반드시 딕셔너리로 바꿔야 합니다.


# ---------------------------------------------------------------
# 7. 실전 - API 응답처럼 생긴 데이터 파싱 연습
# ---------------------------------------------------------------

api_response = """
{
  "response": {
    "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE"},
    "body": {
      "totalCount": 3,
      "items": [
        {"stationName": "종로구", "pm10Value": "45", "pm25Value": "23"},
        {"stationName": "강남구", "pm10Value": "82", "pm25Value": "41"},
        {"stationName": "노원구", "pm10Value": "-",  "pm25Value": "18"}
      ]
    }
  }
}
"""

result = json.loads(api_response)

# 깊이 들어가기
header = result["response"]["header"]
print(f"\n응답 코드: {header['resultCode']} ({header['resultMsg']})")

if header["resultCode"] != "00":
    print("API 호출 실패")
else:
    items = result["response"]["body"]["items"]
    print(f"조회 결과 {len(items)}건\n")

    for item in items:
        station = item["stationName"]
        raw = item["pm10Value"]

        if not raw.isdigit():
            print(f"  {station:<8} 측정값 없음")
            continue

        pm10 = int(raw)
        if pm10 <= 30:
            grade = "좋음"
        elif pm10 <= 80:
            grade = "보통"
        elif pm10 <= 150:
            grade = "나쁨"
        else:
            grade = "매우나쁨"

        print(f"  {station:<8} PM10 {pm10:>3}  {grade}")

# 5일차에는 이 데이터를 실제 서버에서 받아 옵니다.


# ---------------------------------------------------------------
# 8. 자주 나는 에러
# ---------------------------------------------------------------

# 8-1. 작은따옴표를 쓰면 안 됩니다
try:
    json.loads("{'name': '김철수'}")
except json.JSONDecodeError as e:
    print(f"\n작은따옴표 에러: {e}")

# 8-2. 마지막 쉼표
try:
    json.loads('{"a": 1, "b": 2,}')
except json.JSONDecodeError as e:
    print(f"마지막 쉼표 에러: {e}")

# 8-3. 파이썬 객체는 그대로 넣을 수 없습니다
from datetime import datetime
try:
    json.dumps({"now": datetime.now()})
except TypeError as e:
    print(f"변환 불가 에러: {e}")

# 해결: 문자열로 바꿔서 넣습니다
print(json.dumps({"now": datetime.now().isoformat()}, ensure_ascii=False))


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 연락처 목록을 JSON 파일로 저장하고 불러오는 함수를 만드세요.
#
# 2) 위 api_response 에서 PM10 이 가장 높은 지역을 찾으세요.
#
# 3) CSV 파일을 읽어 JSON 으로 변환하는 함수를 만드세요.
#
# 4) 3일차 '학생 성적 관리' 프로그램에 JSON 저장/불러오기를 붙이세요.
