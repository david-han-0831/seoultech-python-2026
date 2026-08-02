"""
5일차 - 02. requests 모듈 사용법

requests 는 파이썬에서 인터넷 요청을 보낼 때 쓰는 표준 도구입니다.
이 파일은 API 키 없이 공개 테스트 서버로 실습합니다.

설치:  pip install requests
"""

import requests

# 테스트용 공개 API (누구나 키 없이 쓸 수 있습니다)
BASE = "https://jsonplaceholder.typicode.com"


# ---------------------------------------------------------------
# 1. 가장 기본 - GET 요청
# ---------------------------------------------------------------

print("=" * 56)
print(" 1. 기본 GET 요청")
print("=" * 56)

response = requests.get(f"{BASE}/users/1")

print(f"상태 코드   : {response.status_code}")
print(f"성공 여부   : {response.ok}")
print(f"응답 형식   : {response.headers.get('Content-Type')}")
print(f"응답 크기   : {len(response.content)} 바이트")
print(f"걸린 시간   : {response.elapsed.total_seconds():.3f}초")


# ---------------------------------------------------------------
# 2. 응답 내용 꺼내기
# ---------------------------------------------------------------

# .text  : 문자열 그대로
print(f"\n[.text 앞 100글자]\n{response.text[:100]}...")

# .json(): JSON 을 파이썬 딕셔너리로 (가장 많이 씁니다)
user = response.json()
print(f"\n[.json()]")
print(f"  이름   : {user['name']}")
print(f"  이메일 : {user['email']}")
print(f"  회사   : {user['company']['name']}")
print(f"  도시   : {user['address']['city']}")

# json.loads(response.text) 와 같은 결과입니다.


# ---------------------------------------------------------------
# 3. params - 질의 문자열을 딕셔너리로 넘기기
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 2. params 사용")
print("=" * 56)

# [나쁜 방법] 직접 문자열을 이어붙이기 - 한글·특수문자에서 깨집니다
# url = BASE + "/posts?userId=1&_limit=3"

# [좋은 방법] params 딕셔너리로 넘기면 알아서 처리해 줍니다
params = {"userId": 1, "_limit": 3}
response = requests.get(f"{BASE}/posts", params=params)

print(f"실제 요청 URL: {response.url}")

posts = response.json()
print(f"\n{len(posts)}건 조회")
for post in posts:
    print(f"  [{post['id']}] {post['title'][:40]}")


# ---------------------------------------------------------------
# 4. 상태 코드 확인 - 반드시 해야 합니다
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 3. 상태 코드 확인")
print("=" * 56)

response = requests.get(f"{BASE}/users/9999")     # 없는 사용자

print(f"상태 코드: {response.status_code}")

if response.status_code == 200:
    print("성공")
elif response.status_code == 404:
    print("→ 그런 데이터가 없습니다.")
else:
    print(f"→ 알 수 없는 오류: {response.status_code}")

# raise_for_status() 를 쓰면 4xx·5xx 일 때 예외를 던집니다.
try:
    response = requests.get(f"{BASE}/users/9999")
    response.raise_for_status()
    print(response.json())
except requests.exceptions.HTTPError as e:
    print(f"HTTPError 발생: {e}")


# ---------------------------------------------------------------
# 5. 타임아웃 - 꼭 넣으세요
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 4. 타임아웃")
print("=" * 56)

# timeout 을 안 주면 서버가 응답을 안 할 때 프로그램이 영원히 멈춥니다.
try:
    response = requests.get(f"{BASE}/users/1", timeout=5)
    print(f"5초 안에 응답받음: {response.status_code}")
except requests.exceptions.Timeout:
    print("시간 초과")


# ---------------------------------------------------------------
# 6. 헤더 붙이기
# ---------------------------------------------------------------

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}
response = requests.get(f"{BASE}/users/1", headers=headers, timeout=5)
print(f"\n헤더를 붙인 요청: {response.status_code}")

# 일부 사이트는 User-Agent 가 없으면 '봇'으로 보고 막습니다.
# 크롤링할 때(05번 파일) 특히 필요합니다.


# ---------------------------------------------------------------
# 7. 모든 예외를 제대로 처리하는 함수
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 5. 안전한 요청 함수")
print("=" * 56)


def fetch_json(url, params=None, timeout=10):
    """URL 에서 JSON 을 받아옵니다.

    성공하면 파싱된 데이터를, 실패하면 None 을 돌려줍니다.
    실무 코드는 이 정도 방어는 반드시 해 둡니다.
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print(f"  [오류] 시간 초과 ({timeout}초)")
    except requests.exceptions.ConnectionError:
        print("  [오류] 연결 실패 - 인터넷 또는 주소를 확인하세요")
    except requests.exceptions.HTTPError as e:
        print(f"  [오류] HTTP {e.response.status_code}")
    except ValueError:
        # .json() 이 실패한 경우 (응답이 JSON 이 아님)
        print("  [오류] 응답이 JSON 형식이 아닙니다")
    except requests.exceptions.RequestException as e:
        print(f"  [오류] 요청 실패: {e}")

    return None


# 정상 요청
data = fetch_json(f"{BASE}/users/2")
if data:
    print(f"  성공: {data['name']}")

# 없는 주소
print("\n없는 주소로 요청:")
data = fetch_json(f"{BASE}/users/9999")
print(f"  결과: {data}")

# 존재하지 않는 도메인
print("\n없는 도메인으로 요청:")
data = fetch_json("https://이런주소는없습니다-12345.com/api")
print(f"  결과: {data}")


# ---------------------------------------------------------------
# 8. 실전 - 여러 건 가져와 가공하기
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 6. 실전 - 사용자 목록 분석")
print("=" * 56)

users = fetch_json(f"{BASE}/users")

if users:
    print(f"\n총 {len(users)}명\n")
    print(f"{'이름':<24}{'도시':<16}{'회사'}")
    print("-" * 66)
    for u in users[:5]:
        print(f"{u['name']:<24}{u['address']['city']:<16}{u['company']['name']}")

    # 도시별 인원 세기
    from collections import Counter
    cities = Counter(u["address"]["city"] for u in users)
    print(f"\n도시 종류: {len(cities)}곳")

    # 이메일 도메인 분석
    domains = Counter(u["email"].split("@")[1] for u in users)
    print("\n[이메일 도메인]")
    for domain, count in domains.most_common(3):
        print(f"  {domain}: {count}명")


# ---------------------------------------------------------------
# 9. 여러 요청을 이어서 - 세션 사용
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 7. Session - 여러 번 요청할 때")
print("=" * 56)

# 같은 서버에 여러 번 요청할 때는 Session 이 더 빠릅니다.
# (연결을 재사용하기 때문입니다)
with requests.Session() as session:
    session.headers.update({"Accept": "application/json"})

    for user_id in [1, 2, 3]:
        r = session.get(f"{BASE}/users/{user_id}", timeout=5)
        if r.ok:
            print(f"  {user_id}: {r.json()['name']}")


# ---------------------------------------------------------------
# 10. 요청 사이에 쉬어 주기 - 매너
# ---------------------------------------------------------------

import time

print("\n[요청 간격 두기]")
for user_id in [4, 5]:
    data = fetch_json(f"{BASE}/users/{user_id}")
    if data:
        print(f"  {data['name']}")
    time.sleep(0.3)     # 0.3초 쉬기

# 짧은 시간에 수백 번 요청하면
#   - 서버에 부담을 줍니다
#   - 429(Too Many Requests) 로 차단당합니다
#   - 심하면 IP 가 막힙니다
# 반복문으로 API 를 부를 때는 반드시 time.sleep() 을 넣으세요.


# ===============================================================
# 연습 문제
# ===============================================================
# 1) https://jsonplaceholder.typicode.com/posts 에서 글 목록을 받아
#    제목이 가장 긴 글을 찾으세요.
#
# 2) 사용자 1번이 쓴 글의 개수를 세어 보세요.
#    (params 로 userId 를 넘기세요)
#
# 3) 사용자 전체를 받아 '이름: 이메일' 형태로 CSV 에 저장하세요.
#    (4일차 csv 모듈 활용)
#
# 4) fetch_json 에 '실패하면 3번까지 다시 시도' 기능을 추가하세요.
