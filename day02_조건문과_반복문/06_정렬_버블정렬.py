"""
2일차 - 06. 정렬 알고리즘 ① 버블 정렬 (Bubble Sort)

아이디어: 옆자리와 비교해서 순서가 잘못되어 있으면 자리를 바꾼다.
         한 바퀴 돌면 가장 큰 값이 맨 뒤로 '떠오른다'(bubble) 해서 붙은 이름.
"""

# ---------------------------------------------------------------
# 1. 두 값의 자리 바꾸기 (swap)
# ---------------------------------------------------------------

a, b = 10, 20
a, b = b, a          # 파이썬은 한 줄이면 됩니다
print(a, b)          # 20 10

# 리스트 안에서도 마찬가지입니다.
lst = [1, 2, 3]
lst[0], lst[2] = lst[2], lst[0]
print(lst)           # [3, 2, 1]


# ---------------------------------------------------------------
# 2. 한 바퀴만 돌려 보기 - 가장 큰 값이 맨 뒤로 간다
# ---------------------------------------------------------------

data = [5, 3, 8, 1, 9, 2]
print(f"\n원본: {data}")

for i in range(len(data) - 1):
    if data[i] > data[i + 1]:
        data[i], data[i + 1] = data[i + 1], data[i]
    print(f"  {i}번과 {i+1}번 비교 후: {data}")

print(f"한 바퀴 후: {data}   ← 가장 큰 9가 맨 뒤로 갔습니다")


# ---------------------------------------------------------------
# 3. 버블 정렬 완성 - 바퀴를 여러 번 돈다
# ---------------------------------------------------------------

def bubble_sort(numbers):
    """버블 정렬로 오름차순 정렬합니다."""
    arr = numbers.copy()     # 원본을 건드리지 않기 위해 복사
    n = len(arr)

    for i in range(n - 1):           # 바퀴 수 : n-1 번이면 충분
        for j in range(n - 1 - i):   # 이미 정렬된 뒤쪽은 볼 필요 없음
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


data = [64, 25, 12, 90, 11, 78]
print(f"\n정렬 전: {data}")
print(f"정렬 후: {bubble_sort(data)}")
print(f"원본 유지: {data}")


# ---------------------------------------------------------------
# 4. 과정을 눈으로 보기
# ---------------------------------------------------------------

def bubble_sort_verbose(numbers):
    """매 바퀴가 끝날 때마다 상태를 출력합니다."""
    arr = numbers.copy()
    n = len(arr)

    print(f"\n시작:      {arr}")
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        # 확정된 뒷부분을 표시
        fixed = arr[n - 1 - i:]
        print(f"{i + 1}바퀴 후:  {arr}   (확정: {fixed})")

    return arr


bubble_sort_verbose([64, 25, 12, 90, 11, 78])


# ---------------------------------------------------------------
# 5. 개선판 - 이미 정렬되어 있으면 일찍 끝내기
# ---------------------------------------------------------------

def bubble_sort_optimized(numbers):
    """한 바퀴 동안 교환이 한 번도 없으면 이미 정렬된 것이므로 중단합니다."""
    arr = numbers.copy()
    n = len(arr)

    for i in range(n - 1):
        swapped = False                    # 이번 바퀴에 교환이 있었나?

        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            print(f"  → {i + 1}바퀴에서 이미 정렬 완료, 조기 종료")
            break

    return arr


print("\n[이미 정렬된 데이터]")
print(bubble_sort_optimized([1, 2, 3, 4, 5]))

print("\n[거꾸로 정렬된 데이터 - 최악의 경우]")
print(bubble_sort_optimized([5, 4, 3, 2, 1]))


# ---------------------------------------------------------------
# 6. 내림차순
# ---------------------------------------------------------------

def bubble_sort_desc(numbers):
    """부등호 방향만 바꾸면 내림차순이 됩니다."""
    arr = numbers.copy()
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] < arr[j + 1]:        # > 에서 < 로만 변경
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


print(f"\n내림차순: {bubble_sort_desc([64, 25, 12, 90, 11, 78])}")


# ---------------------------------------------------------------
# 7. 비교 횟수 세어 보기 - 왜 느린가
# ---------------------------------------------------------------

def bubble_sort_count(numbers):
    arr = numbers.copy()
    n = len(arr)
    compare = 0
    swap = 0

    for i in range(n - 1):
        for j in range(n - 1 - i):
            compare += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap += 1

    return arr, compare, swap


for size in [10, 50, 100]:
    # 거꾸로 정렬된 최악의 데이터
    test = list(range(size, 0, -1))
    _, compare, swap = bubble_sort_count(test)
    print(f"데이터 {size:3d}개 → 비교 {compare:5d}회, 교환 {swap:5d}회")

# 데이터가 10배 늘면 비교 횟수는 약 100배가 됩니다.
# 이런 성질을 O(n²) 이라고 부릅니다. 데이터가 많으면 실무에서 쓰기 어렵습니다.
# 파이썬 내장 sort() 는 훨씬 빠른 알고리즘(Timsort)을 씁니다.


# ---------------------------------------------------------------
# 8. 내장 정렬과 비교
# ---------------------------------------------------------------

import random
import time

data = [random.randint(1, 10000) for _ in range(2000)]

start = time.time()
bubble_sort(data)
bubble_time = time.time() - start

start = time.time()
sorted(data)
builtin_time = time.time() - start

print(f"\n[2000개 정렬 속도 비교]")
print(f"버블 정렬 : {bubble_time:.4f}초")
print(f"내장 sorted(): {builtin_time:.6f}초")
print(f"→ 약 {bubble_time / max(builtin_time, 1e-9):.0f}배 차이")

# 결론: 알고리즘은 '원리를 이해하기 위해' 직접 짜 보고,
#       실무에서는 sorted() / .sort() 를 씁니다.


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 문자열 리스트를 버블 정렬로 가나다순 정렬하세요.
#    (문자열도 > < 로 비교할 수 있습니다)
#
# 2) 학생 딕셔너리 리스트를 점수 기준 버블 정렬하세요.
#    students = [{"name":"김철수","score":88}, ...]
#
# 3) 홀수는 앞쪽, 짝수는 뒤쪽으로 몰되 각각 오름차순이 되게 정렬하세요.
