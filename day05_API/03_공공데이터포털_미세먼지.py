"""
5일차 - 03. 공공데이터포털 API 연동 (미세먼지)

실제 정부 API 를 호출해 실시간 대기오염 정보를 가져옵니다.

[사전 준비]
 1) https://www.data.go.kr 회원가입
 2) '한국환경공단_에어코리아_대기오염정보' 검색 → 활용신청 (즉시 승인)
 3) 마이페이지 → 개발계정 → '일반 인증키(Decoding)' 복사
 4) 프로젝트 루트의 .env 파일에 붙여넣기
      PUBLIC_DATA_API_KEY=여기에붙여넣기

키가 없어도 실행됩니다. 그 경우 샘플 데이터로 동작합니다.
"""

import os

import requests
from dotenv import load_dotenv

# .env 파일을 읽어 환경변수로 올립니다.
# 이 파일이 day05_API 안에 있으므로 상위 폴더의 .env 를 찾습니다.
load_dotenv()
load_dotenv(os.path.join("..", ".env"))

SERVICE_KEY = os.getenv("PUBLIC_DATA_API_KEY")

API_URL = (
    "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc"
    "/getCtprvnRltmMesureDnsty"
)

# 키가 없을 때 쓸 샘플 데이터 (구조는 실제 응답과 같습니다)
SAMPLE_ITEMS = [
    {"stationName": "종로구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "45", "pm25Value": "23", "o3Value": "0.042"},
    {"stationName": "중구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "38", "pm25Value": "19", "o3Value": "0.038"},
    {"stationName": "강남구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "82", "pm25Value": "41", "o3Value": "0.055"},
    {"stationName": "노원구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "-", "pm25Value": "18", "o3Value": "0.031"},
    {"stationName": "송파구", "dataTime": "2026-08-07 13:00",
     "pm10Value": "155", "pm25Value": "88", "o3Value": "0.061"},
]


# ---------------------------------------------------------------
# 1. 등급 판정 - 환경부 기준
# ---------------------------------------------------------------

def grade_pm10(value):
    """미세먼지(PM10) 등급."""
    if value <= 30:
        return "좋음", "🟦"
    if value <= 80:
        return "보통", "🟩"
    if value <= 150:
        return "나쁨", "🟧"
    return "매우나쁨", "🟥"


def grade_pm25(value):
    """초미세먼지(PM2.5) 등급."""
    if value <= 15:
        return "좋음", "🟦"
    if value <= 35:
        return "보통", "🟩"
    if value <= 75:
        return "나쁨", "🟧"
    return "매우나쁨", "🟥"


# ---------------------------------------------------------------
# 2. API 호출
# ---------------------------------------------------------------

def fetch_air_quality(sido="서울", rows=20):
    """공공데이터포털에서 시도별 실시간 대기오염 정보를 가져옵니다.

    Returns:
        측정소 정보 리스트. 실패하면 빈 리스트.
    """
    if not SERVICE_KEY:
        print("[알림] API 키가 없어 샘플 데이터로 진행합니다.")
        print("       .env 파일에 PUBLIC_DATA_API_KEY 를 설정하세요.\n")
        return SAMPLE_ITEMS

    params = {
        "serviceKey": SERVICE_KEY,     # 발급받은 인증키
        "returnType": "json",          # json 또는 xml
        "numOfRows": rows,             # 한 번에 가져올 개수
        "pageNo": 1,
        "sidoName": sido,              # 시도명
        "ver": "1.0",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("[오류] 응답 시간 초과")
        return []
    except requests.exceptions.ConnectionError:
        print("[오류] 연결 실패 - 인터넷을 확인하세요")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"[오류] HTTP {e.response.status_code}")
        return []

    # 공공데이터포털은 키가 틀려도 200 을 주고 XML 에러를 돌려주는 경우가 있습니다.
    try:
        data = response.json()
    except ValueError:
        print("[오류] JSON 이 아닌 응답을 받았습니다. 키를 확인하세요.")
        print(f"       응답 앞부분: {response.text[:200]}")
        return []

    # 응답 구조: response > header / body > items
    header = data.get("response", {}).get("header", {})
    result_code = header.get("resultCode")

    if result_code != "00":
        print(f"[API 오류] {result_code}: {header.get('resultMsg')}")
        print("  30: 등록되지 않은 키   /   22: 요청 한도 초과")
        return []

    return data["response"]["body"]["items"]


# ---------------------------------------------------------------
# 3. 값 정리 - 실무 데이터는 항상 지저분합니다
# ---------------------------------------------------------------

def to_int(value):
    """'45' → 45,  '-' 또는 '' 또는 None → None"""
    if value is None:
        return None
    value = str(value).strip()
    if not value.isdigit():
        return None
    return int(value)


def clean(items):
    """API 응답을 쓰기 좋은 형태로 정리합니다."""
    result = []
    for item in items:
        result.append({
            "station": item.get("stationName", "이름없음"),
            "time": item.get("dataTime", ""),
            "pm10": to_int(item.get("pm10Value")),
            "pm25": to_int(item.get("pm25Value")),
        })
    return result


# ---------------------------------------------------------------
# 4. 출력
# ---------------------------------------------------------------

def print_report(records, sido):
    if not records:
        print("표시할 데이터가 없습니다.")
        return

    time = next((r["time"] for r in records if r["time"]), "-")

    print("=" * 62)
    print(f" {sido} 실시간 대기오염 정보")
    print(f" 측정 시각: {time}")
    print("=" * 62)
    print(f"{'측정소':<12}{'PM10':>8}{'등급':>10}{'PM2.5':>8}{'등급':>10}")
    print("-" * 62)

    for r in records:
        # PM10
        if r["pm10"] is None:
            pm10_text, pm10_grade = "  -", "측정없음"
        else:
            grade, icon = grade_pm10(r["pm10"])
            pm10_text = f"{r['pm10']}"
            pm10_grade = f"{icon}{grade}"

        # PM2.5
        if r["pm25"] is None:
            pm25_text, pm25_grade = "  -", "측정없음"
        else:
            grade, icon = grade_pm25(r["pm25"])
            pm25_text = f"{r['pm25']}"
            pm25_grade = f"{icon}{grade}"

        print(f"{r['station']:<12}{pm10_text:>8}{pm10_grade:>10}"
              f"{pm25_text:>8}{pm25_grade:>10}")

    print("-" * 62)


def print_summary(records):
    """통계를 냅니다. 측정값이 없는 곳은 제외합니다."""
    valid = [r for r in records if r["pm10"] is not None]

    if not valid:
        print("\n집계할 수 있는 데이터가 없습니다.")
        return

    values = [r["pm10"] for r in valid]
    average = sum(values) / len(values)

    worst = max(valid, key=lambda r: r["pm10"])
    best = min(valid, key=lambda r: r["pm10"])

    print(f"\n[요약]  측정소 {len(records)}곳 중 {len(valid)}곳 집계")
    print(f"  평균 PM10 : {average:.1f}㎍/㎥ ({grade_pm10(average)[0]})")
    print(f"  가장 나쁨 : {worst['station']} {worst['pm10']}㎍/㎥")
    print(f"  가장 좋음 : {best['station']} {best['pm10']}㎍/㎥")

    # 등급별 개수
    from collections import Counter
    grades = Counter(grade_pm10(r["pm10"])[0] for r in valid)
    print("\n[등급 분포]")
    for grade in ["좋음", "보통", "나쁨", "매우나쁨"]:
        count = grades.get(grade, 0)
        if count:
            print(f"  {grade:<6} {'■' * count} {count}곳")

    # 주의가 필요한 지역
    bad = [r for r in valid if r["pm10"] > 80]
    if bad:
        print("\n⚠ 외출 시 마스크 권장 지역")
        for r in sorted(bad, key=lambda x: x["pm10"], reverse=True):
            print(f"  {r['station']} (PM10 {r['pm10']})")


# ---------------------------------------------------------------
# 5. 텍스트 막대그래프 - 2주차 matplotlib 맛보기
# ---------------------------------------------------------------

def print_chart(records, limit=10):
    valid = [r for r in records if r["pm10"] is not None]
    if not valid:
        return

    valid.sort(key=lambda r: r["pm10"], reverse=True)
    valid = valid[:limit]

    top = max(r["pm10"] for r in valid)
    scale = 40 / top if top else 1

    print(f"\n[PM10 상위 {len(valid)}곳]")
    for r in valid:
        bar = "█" * max(1, int(r["pm10"] * scale))
        print(f"  {r['station']:<10} {bar} {r['pm10']}")


# ---------------------------------------------------------------
# 실행
# ---------------------------------------------------------------

def main():
    sido = "서울"

    items = fetch_air_quality(sido=sido, rows=25)
    records = clean(items)

    print_report(records, sido)
    print_summary(records)
    print_chart(records)


if __name__ == "__main__":
    main()


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 시도명을 입력받아 조회하도록 바꾸세요.
#    (서울, 부산, 대구, 인천, 광주, 대전, 울산, 경기 ...)
#
# 2) 결과를 CSV 파일로 저장하세요. (4일차 csv 모듈)
#
# 3) 특정 측정소만 골라 조회하는 기능을 추가하세요.
#
# 4) 오존(o3Value)과 초미세먼지도 함께 표시하고,
#    셋 중 하나라도 '나쁨'이면 경고를 띄우세요.
#
# 5) 2주차 예고: 이 데이터를 pandas 로 표로 만들고
#    matplotlib 으로 막대그래프를 그리게 됩니다.
