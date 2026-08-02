"""
5일차 - 05. BeautifulSoup 으로 HTML 파싱

API 가 없는 사이트에서 데이터를 가져와야 할 때 씁니다.
HTML 을 받아 원하는 부분만 뽑아내는 것을 '파싱'이라고 합니다.

설치:  pip install beautifulsoup4

[크롤링 예절 - 반드시 지키세요]
  1. robots.txt 를 확인한다 (사이트주소/robots.txt)
  2. 요청 사이에 time.sleep() 으로 간격을 둔다
  3. 개인정보·저작물을 수집하지 않는다
  4. API 가 있으면 API 를 쓴다
  5. 상업적 이용 전에는 이용약관을 확인한다
"""

import time

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------
# 1. HTML 구조 익히기 - 먼저 문자열로 연습합니다
# ---------------------------------------------------------------

html = """
<html>
  <head><title>파이썬 특강</title></head>
  <body>
    <h1 id="main-title">서울과기대 파이썬 특강</h1>
    <p class="intro">2026년 여름 비교과 프로그램입니다.</p>

    <ul id="curriculum">
      <li class="day" data-num="1">1일차: 기초 문법</li>
      <li class="day" data-num="2">2일차: 조건문과 반복문</li>
      <li class="day" data-num="3">3일차: 함수</li>
      <li class="day" data-num="4">4일차: 클래스와 파일</li>
      <li class="day highlight" data-num="5">5일차: API</li>
    </ul>

    <table id="scores">
      <tr><th>이름</th><th>점수</th></tr>
      <tr><td>김철수</td><td>90</td></tr>
      <tr><td>이영희</td><td>95</td></tr>
      <tr><td>박민수</td><td>77</td></tr>
    </table>

    <a href="https://www.seoultech.ac.kr" class="link">학교 홈페이지</a>
    <a href="https://github.com" class="link">깃허브</a>
  </body>
</html>
"""

# BeautifulSoup 객체 만들기 (두 번째 인자는 파서 종류)
soup = BeautifulSoup(html, "html.parser")


# ---------------------------------------------------------------
# 2. 태그로 찾기
# ---------------------------------------------------------------

print("=" * 56)
print(" 1. 기본 찾기")
print("=" * 56)

# find() : 조건에 맞는 첫 번째 하나
print(soup.find("h1"))              # 태그 통째로
print(soup.find("h1").text)         # 안의 글자만
print(soup.find("h1").get_text())   # 같은 뜻

# find_all() : 조건에 맞는 전부 (리스트로 돌려줍니다)
links = soup.find_all("a")
print(f"\n링크 {len(links)}개")
for a in links:
    print(f"  {a.text} → {a['href']}")     # 속성은 [] 로 꺼냅니다


# ---------------------------------------------------------------
# 3. class / id 로 찾기
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 2. class 와 id 로 찾기")
print("=" * 56)

# class 는 파이썬 예약어라 class_ 로 씁니다
print(soup.find("p", class_="intro").text)

# id 로 찾기
print(soup.find("h1", id="main-title").text)

# 여러 개
days = soup.find_all("li", class_="day")
print(f"\n커리큘럼 {len(days)}일")
for li in days:
    num = li["data-num"]              # 사용자 정의 속성도 꺼낼 수 있습니다
    print(f"  {num}. {li.text}")


# ---------------------------------------------------------------
# 4. CSS 선택자로 찾기 - select
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 3. CSS 선택자 (select)")
print("=" * 56)

# 크롬 개발자도구에서 '선택자 복사'를 하면 이 형태로 나옵니다.
print(soup.select_one("#main-title").text)        # id  → #
print(soup.select_one(".intro").text)             # class → .

print("\n[여러 개 선택]")
for li in soup.select("ul#curriculum li.day"):    # 자손 선택
    print(f"  {li.text}")

print("\n[여러 class 를 동시에 가진 것]")
for li in soup.select("li.day.highlight"):
    print(f"  {li.text}")

print("\n[속성으로 선택]")
print(soup.select_one('li[data-num="3"]').text)

print("\n[링크 주소만]")
print([a["href"] for a in soup.select("a.link")])


# ---------------------------------------------------------------
# 5. 표(table) 파싱 - 실무에서 가장 많이 합니다
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 4. 표 파싱")
print("=" * 56)

table = soup.find("table", id="scores")
rows = table.find_all("tr")

# 첫 줄은 헤더(th)
header = [th.text for th in rows[0].find_all("th")]
print(f"헤더: {header}")

# 나머지는 데이터(td)
data = []
for tr in rows[1:]:
    cells = [td.text for td in tr.find_all("td")]
    data.append({header[0]: cells[0], header[1]: int(cells[1])})

print("\n[파싱 결과]")
for row in data:
    print(f"  {row}")

average = sum(d["점수"] for d in data) / len(data)
print(f"\n평균: {average:.1f}점")
print(f"최고: {max(data, key=lambda d: d['점수'])['이름']}")


# ---------------------------------------------------------------
# 6. 없는 요소를 찾을 때 - 방어 코드
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 5. 없는 요소 처리")
print("=" * 56)

# find 는 없으면 None 을 돌려줍니다.
missing = soup.find("h2")
print(f"h2 태그: {missing}")

# 바로 .text 를 부르면 에러가 납니다.
# print(missing.text)     # AttributeError: 'NoneType' object has no attribute 'text'

# [올바른 방법 1] 확인하고 쓰기
if missing:
    print(missing.text)
else:
    print("h2 태그가 없습니다.")


# [올바른 방법 2] 도우미 함수를 만들어 두기
def safe_text(element, default=""):
    """요소가 없거나 비어 있어도 안전하게 텍스트를 꺼냅니다."""
    if element is None:
        return default
    return element.get_text(strip=True) or default


print(f"안전하게 꺼내기: '{safe_text(soup.find('h2'), '(없음)')}'")
print(f"있는 경우      : '{safe_text(soup.find('h1'))}'")


# ---------------------------------------------------------------
# 7. 실제 웹페이지 가져오기
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 6. 실제 사이트 크롤링")
print("=" * 56)


def fetch_html(url, timeout=10):
    """웹페이지 HTML 을 가져옵니다."""
    headers = {
        # User-Agent 가 없으면 봇으로 보고 막는 사이트가 많습니다.
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # 한글이 깨지면 인코딩을 직접 지정해야 할 때가 있습니다.
        response.encoding = response.apparent_encoding

        return response.text

    except requests.exceptions.RequestException as e:
        print(f"  [오류] {e}")
        return None


# 연습용으로 만들어진 공개 사이트를 씁니다. (크롤링 학습 허용 사이트)
url = "https://books.toscrape.com/"
print(f"요청: {url}")

html_text = fetch_html(url)

if html_text is None:
    print("  페이지를 가져오지 못했습니다. (교내망 차단 가능성)")
    print("  네트워크가 막혀 있어도 위쪽 예제(1~6)는 모두 동작합니다.")
else:
    page = BeautifulSoup(html_text, "html.parser")

    print(f"  페이지 제목: {safe_text(page.find('title'))}")

    books = page.select("article.product_pod")
    print(f"  책 {len(books)}권 발견\n")

    results = []
    for book in books[:10]:
        title = book.h3.a["title"]                      # 제목은 a 태그의 title 속성
        price = safe_text(book.select_one("p.price_color"))
        # 별점은 class 이름에 들어 있습니다. 예) class="star-rating Three"
        rating_class = book.select_one("p.star-rating")["class"]
        rating = rating_class[1] if len(rating_class) > 1 else "?"

        in_stock = "In stock" in safe_text(book.select_one("p.instock"))

        results.append({
            "title": title,
            "price": price,
            "rating": rating,
            "in_stock": in_stock,
        })

    print(f"  {'제목':<44}{'가격':>10}{'별점':>8}")
    print("  " + "-" * 62)
    for r in results:
        title = r["title"][:42]
        print(f"  {title:<44}{r['price']:>10}{r['rating']:>8}")

    # 가격만 숫자로 뽑아 계산해 보기
    prices = []
    for r in results:
        # '£51.77' → 51.77
        digits = "".join(c for c in r["price"] if c.isdigit() or c == ".")
        if digits:
            prices.append(float(digits))

    if prices:
        print(f"\n  평균 가격: £{sum(prices) / len(prices):.2f}")
        print(f"  최고 가격: £{max(prices):.2f}")


# ---------------------------------------------------------------
# 8. 여러 페이지 돌기 - 간격을 꼭 두세요
# ---------------------------------------------------------------

print("\n" + "=" * 56)
print(" 7. 여러 페이지 수집")
print("=" * 56)

all_titles = []

for page_no in range(1, 3):     # 2페이지만
    page_url = f"https://books.toscrape.com/catalogue/page-{page_no}.html"
    print(f"  {page_no}페이지 요청 중...")

    html_text = fetch_html(page_url)
    if html_text is None:
        break

    page = BeautifulSoup(html_text, "html.parser")
    titles = [b.h3.a["title"] for b in page.select("article.product_pod")]
    all_titles.extend(titles)

    print(f"    {len(titles)}건 수집 (누적 {len(all_titles)}건)")

    time.sleep(1)      # ← 반드시! 서버에 부담을 주지 않기 위해

if all_titles:
    print(f"\n  총 {len(all_titles)}건 수집 완료")
    print(f"  첫 번째: {all_titles[0]}")
    print(f"  마지막 : {all_titles[-1]}")


# ---------------------------------------------------------------
# 9. 크롤링이 안 될 때
# ---------------------------------------------------------------
#
#  Q. 브라우저에는 보이는데 코드로 받으면 내용이 비어 있습니다
#     → 자바스크립트로 나중에 그려지는 페이지입니다.
#       requests + BeautifulSoup 으로는 못 가져옵니다.
#       2주차에 배울 Selenium 을 써야 합니다.
#
#  Q. 403 이 뜹니다
#     → User-Agent 헤더를 넣어 보세요. 그래도 안 되면 막아 둔 것입니다.
#
#  Q. 한글이 깨집니다
#     → response.encoding = "utf-8" 또는 "euc-kr" 을 직접 지정해 보세요.
#
#  Q. 선택자를 어떻게 찾나요
#     → 크롬에서 F12 → 원하는 요소 우클릭 → 검사
#       → 다시 우클릭 → Copy → Copy selector


# ===============================================================
# 연습 문제
# ===============================================================
# 1) books.toscrape.com 에서 별점이 Five 인 책만 골라 출력하세요.
#
# 2) 수집한 책 목록을 CSV 로 저장하세요. (4일차 csv 모듈)
#
# 3) 가격이 £30 이하인 책만 필터링하세요.
#
# 4) 카테고리 목록(왼쪽 메뉴)을 수집해 보세요.
#
# 5) 03번의 미세먼지 데이터와 이 크롤링 결과를 각각 JSON 으로 저장하고,
#    다시 불러와 출력하는 코드를 작성하세요.
