"""
5일차 실습 - 미세먼지 알리미

1주차에 배운 모든 것을 모아 만드는 프로그램입니다.

  1일차  변수·자료형·리스트·딕셔너리
  2일차  조건문·반복문
  3일차  함수·컴프리헨션·Counter
  4일차  클래스·예외처리·파일 저장(JSON/CSV)
  5일차  requests·API·JSON 파싱

[기능]
  - 공공데이터포털에서 실시간 대기오염 정보 조회
  - 등급 판정 및 외출 조언
  - 텍스트 그래프로 시각화
  - 조회 이력을 JSON 에 누적 저장
  - CSV 로 내보내기
  - (선택) Gemini 로 안내문 자동 생성
"""

import csv
import json
import os
from collections import Counter
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join("..", ".env"))

PUBLIC_KEY = os.getenv("PUBLIC_DATA_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

AIR_API_URL = (
    "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc"
    "/getCtprvnRltmMesureDnsty"
)
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
    "/gemini-2.0-flash:generateContent"
)

OUTPUT_DIR = "output"
HISTORY_PATH = os.path.join(OUTPUT_DIR, "air_history.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SIDO_LIST = [
    "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
    "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주",
]

SAMPLE_ITEMS = [
    {"stationName": "종로구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "45", "pm25Value": "23"},
    {"stationName": "중구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "38", "pm25Value": "19"},
    {"stationName": "강남구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "82", "pm25Value": "41"},
    {"stationName": "노원구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "-", "pm25Value": "18"},
    {"stationName": "송파구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "155", "pm25Value": "88"},
    {"stationName": "은평구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "28", "pm25Value": "12"},
]


# ===============================================================
# 예외
# ===============================================================

class AirQualityError(Exception):
    """이 프로그램에서 쓰는 예외."""


# ===============================================================
# 모델 - 측정소 한 곳
# ===============================================================

class Station:
    """측정소 한 곳의 대기 정보."""

    PM10_LEVELS = [(30, "좋음", "🟦"), (80, "보통", "🟩"),
                   (150, "나쁨", "🟧"), (float("inf"), "매우나쁨", "🟥")]
    PM25_LEVELS = [(15, "좋음", "🟦"), (35, "보통", "🟩"),
                   (75, "나쁨", "🟧"), (float("inf"), "매우나쁨", "🟥")]

    def __init__(self, name, time, pm10, pm25):
        self.name = name
        self.time = time
        self.pm10 = pm10      # None 일 수 있습니다 (측정값 없음)
        self.pm25 = pm25

    # ---- 생성 ---------------------------------------------------

    @staticmethod
    def _to_int(value):
        """'45' → 45,  '-' / '' / None → None"""
        if value is None:
            return None
        value = str(value).strip()
        return int(value) if value.isdigit() else None

    @classmethod
    def from_api(cls, item):
        """API 응답 한 건을 Station 객체로 만듭니다."""
        return cls(
            name=item.get("stationName", "이름없음"),
            time=item.get("dataTime", ""),
            pm10=cls._to_int(item.get("pm10Value")),
            pm25=cls._to_int(item.get("pm25Value")),
        )

    # ---- 판정 ---------------------------------------------------

    @staticmethod
    def _grade(value, levels):
        if value is None:
            return "측정없음", "⬜"
        for limit, name, icon in levels:
            if value <= limit:
                return name, icon
        return "매우나쁨", "🟥"

    def pm10_grade(self):
        return self._grade(self.pm10, self.PM10_LEVELS)

    def pm25_grade(self):
        return self._grade(self.pm25, self.PM25_LEVELS)

    def is_bad(self):
        """둘 중 하나라도 '나쁨' 이상이면 True."""
        return self.pm10_grade()[0] in ("나쁨", "매우나쁨") \
            or self.pm25_grade()[0] in ("나쁨", "매우나쁨")

    def has_data(self):
        return self.pm10 is not None or self.pm25 is not None

    def advice(self):
        """외출 조언."""
        grade = self.pm10_grade()[0]
        return {
            "좋음": "야외 활동하기 좋습니다.",
            "보통": "무난합니다. 민감군은 장시간 외출을 줄이세요.",
            "나쁨": "마스크(KF80 이상)를 착용하세요.",
            "매우나쁨": "외출을 자제하고 실내 환기도 피하세요.",
            "측정없음": "측정값이 없어 판단할 수 없습니다.",
        }[grade]

    # ---- 저장 ---------------------------------------------------

    def to_dict(self):
        return {
            "name": self.name, "time": self.time,
            "pm10": self.pm10, "pm25": self.pm25,
        }

    def __str__(self):
        pm10 = self.pm10 if self.pm10 is not None else "-"
        grade, icon = self.pm10_grade()
        return f"{self.name} PM10 {pm10} {icon}{grade}"


# ===============================================================
# API 호출
# ===============================================================

def fetch_stations(sido="서울", rows=30):
    """공공데이터포털에서 측정소 목록을 가져옵니다."""
    if not PUBLIC_KEY:
        print("[알림] API 키가 없어 샘플 데이터로 동작합니다.")
        return [Station.from_api(item) for item in SAMPLE_ITEMS]

    params = {
        "serviceKey": PUBLIC_KEY,
        "returnType": "json",
        "numOfRows": rows,
        "pageNo": 1,
        "sidoName": sido,
        "ver": "1.0",
    }

    try:
        response = requests.get(AIR_API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise AirQualityError("응답 시간이 초과되었습니다.")
    except requests.exceptions.ConnectionError:
        raise AirQualityError("인터넷 연결을 확인해 주세요.")
    except requests.exceptions.HTTPError as e:
        raise AirQualityError(f"HTTP 오류 {e.response.status_code}")

    try:
        data = response.json()
    except ValueError:
        raise AirQualityError(
            "JSON 이 아닌 응답을 받았습니다. API 키를 확인하세요.\n"
            f"  응답: {response.text[:150]}"
        )

    header = data.get("response", {}).get("header", {})
    if header.get("resultCode") != "00":
        raise AirQualityError(
            f"API 오류 [{header.get('resultCode')}] {header.get('resultMsg')}"
        )

    items = data["response"]["body"]["items"]
    return [Station.from_api(item) for item in items]


# ===============================================================
# 출력
# ===============================================================

def print_report(stations, sido):
    if not stations:
        print("표시할 데이터가 없습니다.")
        return

    time = next((s.time for s in stations if s.time), "-")

    print("\n" + "=" * 64)
    print(f" {sido} 대기오염 정보   (측정 시각: {time})")
    print("=" * 64)
    print(f"{'측정소':<12}{'PM10':>7}{'등급':>11}{'PM2.5':>8}{'등급':>11}")
    print("-" * 64)

    for s in stations:
        pm10_grade, pm10_icon = s.pm10_grade()
        pm25_grade, pm25_icon = s.pm25_grade()

        pm10 = str(s.pm10) if s.pm10 is not None else "-"
        pm25 = str(s.pm25) if s.pm25 is not None else "-"

        print(f"{s.name:<12}{pm10:>7}{pm10_icon + pm10_grade:>11}"
              f"{pm25:>8}{pm25_icon + pm25_grade:>11}")

    print("-" * 64)


def print_summary(stations):
    valid = [s for s in stations if s.pm10 is not None]

    if not valid:
        print("\n집계할 수 있는 데이터가 없습니다.")
        return

    values = [s.pm10 for s in valid]
    average = sum(values) / len(values)

    worst = max(valid, key=lambda s: s.pm10)
    best = min(valid, key=lambda s: s.pm10)

    print(f"\n[요약]  전체 {len(stations)}곳 / 집계 {len(valid)}곳")
    print(f"  평균 PM10 : {average:.1f}㎍/㎥")
    print(f"  가장 나쁨 : {worst.name} ({worst.pm10})")
    print(f"  가장 좋음 : {best.name} ({best.pm10})")

    grades = Counter(s.pm10_grade()[0] for s in valid)
    print("\n[등급 분포]")
    for grade in ["좋음", "보통", "나쁨", "매우나쁨"]:
        count = grades.get(grade, 0)
        if count:
            ratio = count / len(valid) * 100
            print(f"  {grade:<6} {'■' * count:<12} {count}곳 ({ratio:.0f}%)")

    bad = [s for s in stations if s.is_bad()]
    if bad:
        print(f"\n⚠ 주의 지역 {len(bad)}곳")
        for s in sorted(bad, key=lambda x: x.pm10 or 0, reverse=True):
            print(f"  {s.name}: {s.advice()}")
    else:
        print("\n✓ 전 지역 양호합니다. 야외 활동하기 좋은 날입니다.")


def print_chart(stations, limit=10):
    valid = [s for s in stations if s.pm10 is not None]
    if not valid:
        return

    valid.sort(key=lambda s: s.pm10, reverse=True)
    valid = valid[:limit]

    top = max(s.pm10 for s in valid)
    scale = 38 / top if top else 1

    print(f"\n[PM10 상위 {len(valid)}곳]")
    for s in valid:
        bar = "█" * max(1, int(s.pm10 * scale))
        icon = s.pm10_grade()[1]
        print(f"  {s.name:<10} {icon} {bar} {s.pm10}")


# ===============================================================
# 저장
# ===============================================================

def save_history(sido, stations):
    """조회 결과를 JSON 에 누적 저장합니다."""
    history = load_history()

    history.append({
        "queried_at": datetime.now().isoformat(timespec="seconds"),
        "sido": sido,
        "count": len(stations),
        "stations": [s.to_dict() for s in stations],
    })

    # 최근 50건만 유지
    history = history[-50:]

    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return len(history)


def load_history():
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("[경고] 이력 파일이 손상되어 새로 시작합니다.")
        return []


def print_history():
    history = load_history()

    if not history:
        print("\n저장된 조회 이력이 없습니다.")
        return

    print(f"\n[조회 이력 {len(history)}건]")
    for i, record in enumerate(history[-10:], start=1):
        valid = [s for s in record["stations"] if s["pm10"] is not None]
        avg = sum(s["pm10"] for s in valid) / len(valid) if valid else 0
        print(f"  {i:>2}. {record['queried_at']}  {record['sido']:<4} "
              f"{record['count']}곳  평균 PM10 {avg:.1f}")


def export_csv(stations, sido):
    """결과를 CSV 로 내보냅니다."""
    if not stations:
        raise AirQualityError("내보낼 데이터가 없습니다.")

    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    path = os.path.join(OUTPUT_DIR, f"air_{sido}_{stamp}.csv")

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["측정소", "측정시각", "PM10", "PM10등급",
                         "PM2.5", "PM2.5등급", "조언"])
        for s in stations:
            writer.writerow([
                s.name, s.time,
                s.pm10 if s.pm10 is not None else "",
                s.pm10_grade()[0],
                s.pm25 if s.pm25 is not None else "",
                s.pm25_grade()[0],
                s.advice(),
            ])

    return path


# ===============================================================
# (선택) Gemini 로 안내문 만들기
# ===============================================================

def generate_notice(stations, sido):
    """Gemini API 로 안내 문자를 생성합니다."""
    if not GEMINI_KEY:
        return None

    valid = [s for s in stations if s.pm10 is not None]
    if not valid:
        return None

    lines = "\n".join(f"{s.name} PM10 {s.pm10}, PM2.5 {s.pm25}" for s in valid[:10])

    prompt = f"""아래는 {sido}의 실시간 대기오염 측정값이다.
시민에게 보낼 안내 문자를 2~3문장으로 작성해줘.
과장하지 말고 사실 위주로, 존댓말로 써줘.

{lines}"""

    try:
        response = requests.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": 0.5, "maxOutputTokens": 512}},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"[알림] 안내문 생성 실패: {e}")
        return None


# ===============================================================
# 메인
# ===============================================================

def choose_sido():
    print("\n조회할 지역을 고르세요.")
    for i, sido in enumerate(SIDO_LIST, start=1):
        print(f"{i:>3}. {sido}", end="   ")
        if i % 6 == 0:
            print()
    print()

    while True:
        raw = input("번호 (엔터 = 서울): ").strip()
        if not raw:
            return "서울"
        if raw.isdigit() and 1 <= int(raw) <= len(SIDO_LIST):
            return SIDO_LIST[int(raw) - 1]
        print("  올바른 번호를 입력해 주세요.")


def show_menu():
    print("\n" + "-" * 44)
    print(" 1. 지역 조회        2. 다른 지역 조회")
    print(" 3. CSV 내보내기     4. 조회 이력")
    print(" 5. AI 안내문 생성   0. 종료")
    print("-" * 44)


def main():
    print("=" * 64)
    print(" 미세먼지 알리미  v1.0")
    print(" 서울과기대 파이썬 특강 1주차 종합 실습")
    print("=" * 64)

    if not PUBLIC_KEY:
        print("\n※ 공공데이터포털 API 키가 없어 샘플 데이터로 동작합니다.")
        print("  .env 에 PUBLIC_DATA_API_KEY 를 설정하면 실제 데이터를 봅니다.")

    sido = "서울"
    stations = []

    while True:
        show_menu()
        choice = input("메뉴 선택: ").strip()

        if choice in ("1", "2"):
            if choice == "2":
                sido = choose_sido()

            try:
                print(f"\n{sido} 지역 조회 중...")
                stations = fetch_stations(sido)

                print_report(stations, sido)
                print_summary(stations)
                print_chart(stations)

                count = save_history(sido, stations)
                print(f"\n(조회 이력 저장 완료 - 총 {count}건)")

            except AirQualityError as e:
                print(f"\n[오류] {e}")

        elif choice == "3":
            try:
                path = export_csv(stations, sido)
                print(f"\nCSV 저장 완료: {path}")
            except AirQualityError as e:
                print(f"\n[오류] {e}")

        elif choice == "4":
            print_history()

        elif choice == "5":
            if not stations:
                print("\n먼저 지역을 조회해 주세요.")
                continue

            if not GEMINI_KEY:
                print("\nGEMINI_API_KEY 가 설정되지 않았습니다.")
                print("https://aistudio.google.com/apikey 에서 발급받으세요.")
                continue

            print("\n안내문 생성 중...")
            notice = generate_notice(stations, sido)
            if notice:
                print("\n" + "=" * 64)
                print(" AI 생성 안내문")
                print("=" * 64)
                print(f" {notice}")
                print("=" * 64)

        elif choice == "0":
            print("\n프로그램을 종료합니다. 수고하셨습니다!")
            break

        else:
            print("0~5 중에서 선택해 주세요.")


if __name__ == "__main__":
    main()


# ===============================================================
# 더 해보기 (2주차로 이어집니다)
# ===============================================================
# 1) 여러 지역을 한 번에 조회해 비교하는 기능을 만드세요.
# 2) 조회 이력을 이용해 '어제보다 나빠졌는지' 알려 주세요.
# 3) 특정 지역의 PM10 이 기준을 넘으면 경고를 띄우는 감시 모드를 만드세요.
# 4) [2주차] pandas 로 이력 데이터를 표로 만들어 분석해 보세요.
# 5) [2주차] matplotlib 으로 지역별 막대그래프와 시간대별 추이 선그래프를
#    그려 보세요.
