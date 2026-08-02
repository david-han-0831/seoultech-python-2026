"""
3일차 - 06. 리팩토링 실습 - 2일차 정렬 코드를 함수로 정리하기

리팩토링(refactoring)이란
'동작은 그대로 두고 코드의 구조만 개선하는 것'입니다.

2일차에 쓴 정렬 코드를 단계별로 다듬어 봅니다.
"""

import random

# ===============================================================
# [0단계] 처음 짠 코드 - 동작은 하지만 문제가 많습니다
# ===============================================================

data = [64, 25, 12, 90, 11]

# 문제점
#  1) 재사용할 수 없다 (다른 리스트에 쓰려면 복사·붙여넣기)
#  2) 원본을 망가뜨린다
#  3) 내림차순이 필요하면 코드를 또 짜야 한다
#  4) 무슨 일을 하는지 설명이 없다
for i in range(len(data) - 1):
    for j in range(len(data) - 1 - i):
        if data[j] > data[j + 1]:
            data[j], data[j + 1] = data[j + 1], data[j]
print("0단계:", data)


# ===============================================================
# [1단계] 함수로 묶기 - 재사용 가능하게
# ===============================================================

def bubble_sort_v1(arr):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


data = [64, 25, 12, 90, 11]
print("1단계:", bubble_sort_v1(data))
print("  원본:", data, "← 아직 원본이 바뀝니다")


# ===============================================================
# [2단계] 원본 보호 - 복사본을 만들어 작업
# ===============================================================

def bubble_sort_v2(numbers):
    arr = numbers.copy()
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


data = [64, 25, 12, 90, 11]
print("\n2단계:", bubble_sort_v2(data))
print("  원본:", data, "← 그대로 유지됩니다")


# ===============================================================
# [3단계] 오름/내림 선택 가능하게 - 옵션 추가
# ===============================================================

def bubble_sort_v3(numbers, reverse=False):
    arr = numbers.copy()
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            # 조건을 한 줄로 처리
            should_swap = arr[j] < arr[j + 1] if reverse else arr[j] > arr[j + 1]
            if should_swap:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


print("\n3단계 오름차순:", bubble_sort_v3(data))
print("3단계 내림차순:", bubble_sort_v3(data, reverse=True))


# ===============================================================
# [4단계] 정렬 기준을 밖에서 정하게 - key 함수 도입
# ===============================================================

def bubble_sort(numbers, key=None, reverse=False):
    """버블 정렬로 리스트를 정렬합니다.

    Args:
        numbers: 정렬할 리스트 (원본은 변경되지 않습니다)
        key: 비교에 쓸 값을 뽑는 함수. None 이면 값 자체를 비교합니다.
        reverse: True 면 내림차순

    Returns:
        정렬된 새 리스트
    """
    arr = numbers.copy()

    # key 가 없으면 '값 자체를 돌려주는 함수'를 기본으로 씁니다.
    if key is None:
        key = lambda x: x

    n = len(arr)
    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            left = key(arr[j])
            right = key(arr[j + 1])

            if (left < right) if reverse else (left > right):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:      # 이미 정렬됐으면 조기 종료
            break

    return arr


# 이제 무엇이든 정렬할 수 있습니다.
print("\n[4단계 - 완성판]")

numbers = [64, 25, 12, 90, 11]
print("숫자:", bubble_sort(numbers))

words = ["banana", "kiwi", "apple", "watermelon"]
print("문자열 가나다순:", bubble_sort(words))
print("문자열 길이순:", bubble_sort(words, key=len))

students = [
    {"name": "김철수", "score": 88, "age": 21},
    {"name": "이영희", "score": 95, "age": 20},
    {"name": "박민수", "score": 70, "age": 23},
]
by_score = bubble_sort(students, key=lambda s: s["score"], reverse=True)
print("학생 점수순:", [s["name"] for s in by_score])

by_age = bubble_sort(students, key=lambda s: s["age"])
print("학생 나이순:", [s["name"] for s in by_age])


# ===============================================================
# [5단계] 검증하기 - 내장 sorted() 와 결과가 같은지 확인
# ===============================================================

print("\n[검증]")

for trial in range(5):
    test = [random.randint(1, 100) for _ in range(20)]

    mine = bubble_sort(test)
    builtin = sorted(test)

    ok = mine == builtin
    print(f"  테스트 {trial + 1}: {'통과' if ok else '실패'}")
    if not ok:
        print(f"    내 결과 : {mine}")
        print(f"    정답    : {builtin}")

# 엣지 케이스도 확인합니다.
print("\n[엣지 케이스]")
print("  빈 리스트   :", bubble_sort([]))
print("  값 하나     :", bubble_sort([42]))
print("  전부 같은 값:", bubble_sort([7, 7, 7]))
print("  이미 정렬됨 :", bubble_sort([1, 2, 3, 4]))
print("  거꾸로      :", bubble_sort([4, 3, 2, 1]))
print("  음수 포함   :", bubble_sort([3, -1, 0, -5, 2]))


# ===============================================================
# 리팩토링 원칙 정리
# ===============================================================
#
# 1) 같은 코드를 두 번 쓰게 되면 → 함수로 만든다
# 2) 함수는 한 가지 일만 한다
# 3) 원본 데이터는 함부로 바꾸지 않는다
# 4) 바뀔 수 있는 부분은 매개변수로 뺀다 (reverse, key)
# 5) 함수 이름과 독스트링으로 '무엇을 하는지' 설명한다
# 6) 고친 뒤에는 반드시 '결과가 같은지' 확인한다
#
# 그리고 가장 중요한 것:
#   실무에서는 sorted() 를 씁니다.
#   직접 짜 보는 이유는 '안에서 무슨 일이 일어나는지' 알기 위해서입니다.


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 위 bubble_sort 를 참고해 insertion_sort 도 같은 형태로
#    (key, reverse 지원) 리팩토링하세요.
#
# 2) 2일차에 만든 '숫자 맞추기 게임'에서 반복되는 부분을 찾아
#    함수로 정리해 보세요.
#
# 3) 아래 코드를 리팩토링하세요.
#    scores = [88, 95, 70]
#    print("평균:", (88+95+70)/3)
#    print("최고:", 95)
#    → 값이 바뀌어도 동작하도록 함수로 만드세요.
