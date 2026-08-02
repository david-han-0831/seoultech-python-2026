"""
2일차 - 07. 정렬 알고리즘 ② 삽입 정렬 (Insertion Sort)

아이디어: 카드 게임에서 손패를 정리하는 방식과 같습니다.
         왼쪽은 이미 정렬되어 있다고 보고,
         새 카드를 왼쪽의 알맞은 자리에 '끼워 넣는다'.
"""

# ---------------------------------------------------------------
# 1. 손으로 따라가 보기
# ---------------------------------------------------------------
#
#  [5]  3  8  1        ← 5는 혼자니까 이미 정렬됨
#  [3 5]  8  1         ← 3을 5 앞에 끼워 넣음
#  [3 5 8]  1          ← 8은 제자리
#  [1 3 5 8]           ← 1을 맨 앞까지 밀어 넣음


# ---------------------------------------------------------------
# 2. 기본 구현
# ---------------------------------------------------------------

def insertion_sort(numbers):
    """삽입 정렬로 오름차순 정렬합니다."""
    arr = numbers.copy()

    # 0번은 이미 정렬된 것으로 보고 1번부터 시작합니다.
    for i in range(1, len(arr)):
        key = arr[i]        # 이번에 끼워 넣을 값
        j = i - 1           # 바로 왼쪽부터 살펴봄

        # key 보다 큰 값들을 오른쪽으로 한 칸씩 밀어냅니다.
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # 밀어내고 생긴 빈자리에 key 를 넣습니다.
        arr[j + 1] = key

    return arr


data = [64, 25, 12, 90, 11, 78]
print(f"정렬 전: {data}")
print(f"정렬 후: {insertion_sort(data)}")


# ---------------------------------------------------------------
# 3. 과정을 눈으로 보기
# ---------------------------------------------------------------

def insertion_sort_verbose(numbers):
    arr = numbers.copy()
    print(f"\n시작:  {arr}")

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        print(f"\n[{i}단계] {key} 를 왼쪽 {arr[:i]} 안에 끼워 넣습니다")

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            print(f"   {arr[j]} 를 오른쪽으로 밀기 → {arr}")
            j -= 1

        arr[j + 1] = key
        print(f"   {key} 를 {j + 1}번 자리에 넣기 → {arr}")

    return arr


insertion_sort_verbose([64, 25, 12, 90, 11])


# ---------------------------------------------------------------
# 4. 내림차순
# ---------------------------------------------------------------

def insertion_sort_desc(numbers):
    arr = numbers.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key:     # > 를 < 로만 변경
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


print(f"\n내림차순: {insertion_sort_desc([64, 25, 12, 90, 11, 78])}")


# ---------------------------------------------------------------
# 5. 버블 정렬과 비교
# ---------------------------------------------------------------

def bubble_sort_count(numbers):
    arr = numbers.copy()
    n = len(arr)
    compare = 0
    for i in range(n - 1):
        for j in range(n - 1 - i):
            compare += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return compare


def insertion_sort_count(numbers):
    arr = numbers.copy()
    compare = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            compare += 1
            arr[j + 1] = arr[j]
            j -= 1
        if j >= 0:
            compare += 1
        arr[j + 1] = key
    return compare


print("\n[비교 횟수 - 데이터 상태에 따라]")

almost_sorted = [1, 2, 3, 4, 5, 6, 7, 9, 8]     # 거의 정렬됨
reversed_data = [9, 8, 7, 6, 5, 4, 3, 2, 1]     # 완전히 거꾸로

print(f"거의 정렬된 데이터")
print(f"  버블 : {bubble_sort_count(almost_sorted)}회")
print(f"  삽입 : {insertion_sort_count(almost_sorted)}회   ← 훨씬 적습니다")

print(f"거꾸로 된 데이터")
print(f"  버블 : {bubble_sort_count(reversed_data)}회")
print(f"  삽입 : {insertion_sort_count(reversed_data)}회")

# 정리
#  - 둘 다 최악의 경우 O(n²) 입니다.
#  - 하지만 삽입 정렬은 '이미 어느 정도 정렬된 데이터'에서 매우 빠릅니다.
#  - 그래서 실제 라이브러리(Timsort)도 작은 구간에서는 삽입 정렬을 씁니다.


# ---------------------------------------------------------------
# 6. 응용 - 정렬된 리스트에 값 하나 끼워 넣기
# ---------------------------------------------------------------

def insert_into_sorted(sorted_list, value):
    """이미 정렬된 리스트에 값을 올바른 위치에 넣습니다."""
    arr = sorted_list.copy()
    arr.append(value)

    i = len(arr) - 1
    while i > 0 and arr[i - 1] > arr[i]:
        arr[i - 1], arr[i] = arr[i], arr[i - 1]
        i -= 1

    return arr


ranking = [10, 20, 30, 40, 50]
print(f"\n{ranking} 에 35 삽입 → {insert_into_sorted(ranking, 35)}")

# 표준 라이브러리에도 같은 기능이 있습니다.
import bisect
scores = [10, 20, 30, 40, 50]
bisect.insort(scores, 35)
print(f"bisect.insort 사용 → {scores}")


# ---------------------------------------------------------------
# 7. 실전 - 학생 성적 순위표 만들기
# ---------------------------------------------------------------

students = [
    {"name": "김철수", "score": 88},
    {"name": "이영희", "score": 95},
    {"name": "박민수", "score": 70},
    {"name": "최지우", "score": 100},
    {"name": "정하늘", "score": 62},
]


def insertion_sort_students(data):
    """점수 내림차순으로 삽입 정렬합니다."""
    arr = data.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j]["score"] < key["score"]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


print("\n[성적 순위표]")
for rank, s in enumerate(insertion_sort_students(students), start=1):
    print(f"{rank}등  {s['name']:<8} {s['score']:>4}점")


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 삽입 정렬로 문자열 리스트를 길이순으로 정렬하세요.
#
# 2) 삽입 정렬 코드에 '몇 번 이동했는지' 세는 기능을 추가하세요.
#
# 3) 선택 정렬(Selection Sort)을 직접 구현해 보세요.
#    아이디어: 남은 것 중 가장 작은 값을 찾아 맨 앞과 교환하기
