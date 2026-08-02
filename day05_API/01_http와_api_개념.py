"""
5일차 - 01. HTTP 와 API 개념

지금까지는 내 컴퓨터 안의 데이터만 다뤘습니다.
오늘부터는 인터넷 너머의 데이터를 가져옵니다.

이 파일은 개념 정리입니다. 실행하면 설명이 순서대로 출력됩니다.
"""

# ---------------------------------------------------------------
# 1. API 란 무엇인가
# ---------------------------------------------------------------
#
#  API (Application Programming Interface)
#    = 프로그램끼리 데이터를 주고받는 약속된 창구
#
#  식당에 비유하면
#    - 손님(내 프로그램)  : "미세먼지 데이터 주세요"
#    - 메뉴판(API 문서)   : 무엇을 어떻게 주문할 수 있는지 적혀 있음
#    - 주방(서버)         : 실제로 데이터를 가지고 있는 곳
#    - 종업원(API)        : 주문을 받아 주방에 전하고 결과를 가져옴
#
#  사람은 브라우저로 웹사이트를 봅니다 (HTML - 사람이 보기 좋은 형태).
#  프로그램은 API 로 데이터를 받습니다 (JSON - 컴퓨터가 읽기 좋은 형태).


# ---------------------------------------------------------------
# 2. URL 뜯어보기
# ---------------------------------------------------------------

from urllib.parse import urlparse, parse_qs, urlencode

url = "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=abc123&sidoName=서울&returnType=json&numOfRows=10"

parsed = urlparse(url)

print("=" * 60)
print(" URL 구조 뜯어보기")
print("=" * 60)
print(f"  프로토콜(scheme) : {parsed.scheme}")
print(f"  주소(host)       : {parsed.netloc}")
print(f"  경로(path)       : {parsed.path}")
print(f"  질의(query)      : {parsed.query}")

print("\n  질의 문자열을 딕셔너리로 풀면:")
for key, value in parse_qs(parsed.query).items():
    print(f"    {key} = {value[0]}")

# 반대로 딕셔너리를 질의 문자열로 만들 수도 있습니다.
params = {"sidoName": "서울", "numOfRows": 10, "returnType": "json"}
print(f"\n  딕셔너리 → 질의 문자열: {urlencode(params)}")

# requests 라이브러리를 쓰면 이걸 직접 만들 필요가 없습니다.
# params 딕셔너리만 넘기면 알아서 붙여 줍니다. (다음 파일에서)


# ---------------------------------------------------------------
# 3. HTTP 메서드
# ---------------------------------------------------------------

print("\n" + "=" * 60)
print(" HTTP 메서드 - 서버에 무엇을 요청하는가")
print("=" * 60)

methods = [
    ("GET",    "데이터를 조회한다",       "게시글 목록 보기"),
    ("POST",   "새 데이터를 만든다",      "회원가입, 글쓰기"),
    ("PUT",    "데이터를 통째로 바꾼다",  "프로필 전체 수정"),
    ("PATCH",  "데이터 일부를 바꾼다",    "닉네임만 수정"),
    ("DELETE", "데이터를 지운다",         "글 삭제"),
]

for method, meaning, example in methods:
    print(f"  {method:<8} {meaning:<20} 예) {example}")

print("\n  이 수업에서는 GET 만 씁니다. (데이터 조회)")


# ---------------------------------------------------------------
# 4. 상태 코드 (Status Code)
# ---------------------------------------------------------------

print("\n" + "=" * 60)
print(" 상태 코드 - 요청이 어떻게 됐는지 알려주는 숫자")
print("=" * 60)

codes = [
    (200, "OK",                    "성공 ✓"),
    (201, "Created",               "만들어짐"),
    (301, "Moved Permanently",     "주소가 바뀜"),
    (400, "Bad Request",           "요청이 잘못됨 (내 잘못)"),
    (401, "Unauthorized",          "인증 필요 (키가 없음)"),
    (403, "Forbidden",             "권한 없음 (키는 있는데 자격 부족)"),
    (404, "Not Found",             "그런 주소 없음"),
    (429, "Too Many Requests",     "너무 자주 요청함"),
    (500, "Internal Server Error", "서버가 고장남 (서버 잘못)"),
    (503, "Service Unavailable",   "서버 점검 중"),
]

for code, name, meaning in codes:
    if code < 300:
        mark = "🟢"
    elif code < 400:
        mark = "🔵"
    elif code < 500:
        mark = "🟡"
    else:
        mark = "🔴"
    print(f"  {mark} {code}  {name:<24} {meaning}")

print("\n  외우는 법")
print("    2xx  잘 됐다")
print("    3xx  다른 데로 가라")
print("    4xx  네(클라이언트)가 잘못했다")
print("    5xx  내(서버)가 잘못했다")


# ---------------------------------------------------------------
# 5. 응답 형식 - JSON vs HTML
# ---------------------------------------------------------------

print("\n" + "=" * 60)
print(" 응답 형식")
print("=" * 60)

print("""
  [JSON - API 가 주는 형태]
  {
    "stationName": "종로구",
    "pm10Value": "45",
    "dataTime": "2026-08-07 13:00"
  }
  → json.loads() 로 바로 딕셔너리가 됩니다. 다루기 쉽습니다.

  [HTML - 웹페이지]
  <div class="station">
    <span class="name">종로구</span>
    <span class="value">45</span>
  </div>
  → BeautifulSoup 으로 원하는 부분만 뽑아내야 합니다. (05번 파일)

  가능하면 API(JSON)를 쓰세요.
  API 가 없을 때만 크롤링(HTML 파싱)을 합니다.
""")


# ---------------------------------------------------------------
# 6. API 키는 왜 필요한가
# ---------------------------------------------------------------

print("=" * 60)
print(" API 키")
print("=" * 60)

print("""
  대부분의 API 는 '누가 얼마나 쓰는지' 알기 위해 키를 요구합니다.
  키는 비밀번호와 같습니다.

  [절대 하지 말 것]
    - 코드에 키를 직접 적어서 깃허브에 올리기
      SERVICE_KEY = "abcd1234..."      ← 위험!
    - 키를 캡처해서 카톡·메일로 공유하기

  [올바른 방법]
    1) .env 파일에 적는다
         PUBLIC_DATA_API_KEY=abcd1234...
    2) .gitignore 에 .env 를 넣는다  (이미 넣어 두었습니다)
    3) 코드에서는 os.getenv() 로 읽는다
         key = os.getenv("PUBLIC_DATA_API_KEY")

  실수로 키를 올렸다면 → 즉시 그 키를 폐기하고 새로 발급받으세요.
  파일에서 지우는 것만으로는 부족합니다. 커밋 기록에 남습니다.
""")


# ---------------------------------------------------------------
# 7. 오늘 쓸 API 와 키 발급처
# ---------------------------------------------------------------

print("=" * 60)
print(" 오늘 실습에 필요한 준비")
print("=" * 60)

print("""
  1. 라이브러리 설치 (프로젝트 루트에서)
       pip install -r requirements.txt

  2. 공공데이터포털 키 발급
       https://www.data.go.kr
       회원가입 → '한국환경공단 대기오염정보' 검색 → 활용신청
       → 마이페이지에서 '일반 인증키(Decoding)' 복사
       ※ 승인까지 몇 분~1시간 걸릴 수 있습니다

  3. Gemini API 키 발급
       https://aistudio.google.com/apikey
       구글 로그인 → Create API key

  4. .env 파일 만들기 (프로젝트 루트)
       .env.example 을 복사해 .env 로 이름을 바꾸고 키를 채워 넣으세요
         Windows : copy .env.example .env

  키가 아직 없어도 02번, 05번 파일은 실행됩니다.
  (공개 테스트 API 를 쓰기 때문입니다)
""")

print("=" * 60)


# ===============================================================
# 생각해 보기
# ===============================================================
# 1) 평소 쓰는 앱 중에서 API 를 쓰고 있을 것 같은 기능을 찾아보세요.
#    (날씨 위젯, 지도, 로그인, 결제...)
#
# 2) 브라우저에서 아래 주소를 열어 JSON 이 어떻게 생겼는지 보세요.
#    https://jsonplaceholder.typicode.com/users/1
#
# 3) 크롬 개발자도구(F12) → Network 탭을 켜고 아무 사이트나 새로고침해
#    어떤 요청들이 오가는지 살펴보세요.
