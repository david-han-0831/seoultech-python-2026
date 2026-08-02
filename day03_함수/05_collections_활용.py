"""
3일차 - 05. collections - 반복 작업을 한 줄로 줄여 주는 표준 도구

지금까지 직접 만들었던 '개수 세기', '그룹으로 묶기' 같은 작업을
파이썬이 미리 만들어 둔 도구로 처리합니다.
설치가 필요 없는 표준 라이브러리입니다.
"""

from collections import Counter, defaultdict, deque

# ---------------------------------------------------------------
# 1. Counter - 개수 세기
# ---------------------------------------------------------------

# [기존 방식] 1일차에 했던 방법
text = "banana"
manual = {}
for c in text:
    manual[c] = manual.get(c, 0) + 1
print(manual)

# [Counter] 한 줄이면 됩니다
counter = Counter(text)
print(counter)              # Counter({'a': 3, 'n': 2, 'b': 1})
print(counter["a"])         # 3
print(counter["z"])         # 0  ← 없는 키를 물어도 에러 없이 0

# 가장 많이 나온 것부터
print(counter.most_common())      # [('a',3), ('n',2), ('b',1)]
print(counter.most_common(2))     # 상위 2개만


# 실전: 단어 빈도수
sentence = "python is easy python is powerful python is popular"
word_count = Counter(sentence.split())
print("\n[단어 빈도]")
for word, count in word_count.most_common():
    print(f"  {word:<10} {'█' * count} {count}회")

# 실전: 설문 결과 집계
votes = ["파이썬", "자바", "파이썬", "자바스크립트", "파이썬", "자바"]
result = Counter(votes)
print(f"\n총 {sum(result.values())}표")
for lang, count in result.most_common():
    ratio = count / sum(result.values()) * 100
    print(f"  {lang:<12} {count}표 ({ratio:.1f}%)")

winner, top_votes = result.most_common(1)[0]
print(f"1위: {winner} ({top_votes}표)")

# Counter 끼리 연산도 됩니다
a = Counter("hello")
b = Counter("world")
print(a + b)     # 합치기
print(a - b)     # 빼기


# ---------------------------------------------------------------
# 2. defaultdict - 없는 키를 자동으로 만들어 주기
# ---------------------------------------------------------------

students = [
    {"name": "김철수", "major": "ITM"},
    {"name": "이영희", "major": "ITM"},
    {"name": "박민수", "major": "산업공학"},
    {"name": "최지우", "major": "ITM"},
]

# [기존 방식] 키가 있는지 매번 확인해야 합니다
manual = {}
for s in students:
    if s["major"] not in manual:
        manual[s["major"]] = []
    manual[s["major"]].append(s["name"])
print(manual)

# [defaultdict] 없는 키를 부르면 자동으로 빈 리스트가 생깁니다
grouped = defaultdict(list)
for s in students:
    grouped[s["major"]].append(s["name"])
print(dict(grouped))

# 숫자를 세는 용도라면 int
count = defaultdict(int)
for s in students:
    count[s["major"]] += 1          # 없는 키는 자동으로 0에서 시작
print(dict(count))

# 집합으로 모으기 (중복 자동 제거)
tags = defaultdict(set)
tags["파이썬"].add("초급")
tags["파이썬"].add("초급")
tags["파이썬"].add("중급")
print(dict(tags))


# ---------------------------------------------------------------
# 3. deque - 양쪽 끝에서 빠르게 넣고 빼기
# ---------------------------------------------------------------

# 리스트는 맨 앞에 넣고 빼는 게 느립니다. (뒤 요소를 전부 밀어야 해서)
# deque 는 양쪽 끝 모두 빠릅니다.

queue = deque(["첫번째", "두번째"])

queue.append("맨뒤 추가")
queue.appendleft("맨앞 추가")
print(queue)

print(queue.pop())        # 맨 뒤에서 꺼내기
print(queue.popleft())    # 맨 앞에서 꺼내기
print(queue)

# 실전: 최근 기록 5개만 유지 (오래된 건 자동으로 밀려남)
recent = deque(maxlen=5)
for i in range(1, 9):
    recent.append(f"작업{i}")
print(f"\n최근 5개: {list(recent)}")

# 실전: 대기열 시뮬레이션
waiting = deque(["김철수", "이영희", "박민수"])
print(f"\n대기: {list(waiting)}")
while waiting:
    person = waiting.popleft()
    print(f"  {person} 님 입장 (남은 대기 {len(waiting)}명)")


# ---------------------------------------------------------------
# 4. 실전 종합 - 로그 분석
# ---------------------------------------------------------------

logs = [
    "2026-08-03 13:05 INFO  김철수 로그인",
    "2026-08-03 13:07 ERROR 이영희 로그인실패",
    "2026-08-03 13:08 INFO  박민수 로그인",
    "2026-08-03 13:12 ERROR 이영희 로그인실패",
    "2026-08-03 13:15 WARN  김철수 세션만료",
    "2026-08-03 13:20 ERROR 이영희 로그인실패",
    "2026-08-03 13:22 INFO  이영희 로그인",
]

print("\n" + "=" * 40)
print(" 로그 분석 결과")
print("=" * 40)

levels = Counter()
users = Counter()
user_actions = defaultdict(list)

for line in logs:
    parts = line.split()
    # ['2026-08-03', '13:05', 'INFO', '김철수', '로그인']
    time = parts[1]
    level = parts[2]
    user = parts[3]
    action = parts[4]

    levels[level] += 1
    users[user] += 1
    user_actions[user].append(f"{time} {action}")

print("\n[레벨별 건수]")
for level, count in levels.most_common():
    print(f"  {level:<6} {count}건")

print("\n[사용자별 활동 수]")
for user, count in users.most_common():
    print(f"  {user}: {count}건")

print("\n[사용자별 상세]")
for user, actions in user_actions.items():
    print(f"  {user}")
    for a in actions:
        print(f"    - {a}")

# 에러가 3번 이상인 사용자 찾기
error_users = Counter(
    line.split()[3] for line in logs if "ERROR" in line
)
print("\n[주의 필요 사용자 - 에러 3회 이상]")
for user, count in error_users.items():
    if count >= 3:
        print(f"  ⚠ {user}: 에러 {count}회")


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 문장을 입력받아 가장 많이 쓰인 글자 3개를 출력하세요. (공백 제외)
#
# 2) 아래 판매 데이터를 상품별 총 판매량으로 집계하세요.
#    sales = [("커피",2), ("케이크",1), ("커피",3), ("주스",2), ("커피",1)]
#
# 3) 학생 리스트를 학년별로 그룹핑해 출력하세요. (defaultdict 사용)
#
# 4) deque 로 '최근 검색어 10개' 기능을 만들어 보세요.
#    같은 검색어를 다시 입력하면 맨 앞으로 올라오게 하세요.
