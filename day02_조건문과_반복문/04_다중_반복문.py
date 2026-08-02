"""
2일차 - 04. 다중 반복문 (중첩 반복문)

반복문 안에 반복문을 넣는 것입니다.
표·격자처럼 '가로 × 세로' 구조를 다루거나 모든 조합을 만들 때 씁니다.
"""

# ---------------------------------------------------------------
# 1. 동작 원리
# ---------------------------------------------------------------

# 바깥이 한 바퀴 돌 때마다 안쪽은 전부 돕니다.
for i in range(3):          # 바깥 : 3번
    for j in range(2):      # 안쪽 : 매번 2번씩
        print(f"i={i}, j={j}")
    print("---")            # 안쪽 반복이 끝날 때마다 실행

# 총 실행 횟수 = 3 × 2 = 6번


# ---------------------------------------------------------------
# 2. 구구단 전체
# ---------------------------------------------------------------

for dan in range(2, 10):
    print(f"\n[{dan}단]")
    for i in range(1, 10):
        print(f"{dan} x {i} = {dan * i:2d}")

# 가로로 펼쳐서 보기 좋게
print("\n[구구단 표]")
for i in range(1, 10):
    for dan in range(2, 10):
        print(f"{dan}x{i}={dan * i:2d}", end="  ")
    print()   # 한 줄 끝


# ---------------------------------------------------------------
# 3. 별 찍기 - 중첩 반복문의 단골 연습
# ---------------------------------------------------------------

n = 5

print("\n[직각삼각형]")
for i in range(1, n + 1):
    for _ in range(i):
        print("*", end="")
    print()

print("\n[역삼각형]")
for i in range(n, 0, -1):
    print("*" * i)

print("\n[가운데 정렬 삼각형]")
for i in range(1, n + 1):
    spaces = " " * (n - i)
    stars = "*" * (2 * i - 1)
    print(spaces + stars)

print("\n[다이아몬드]")
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))
for i in range(n - 1, 0, -1):
    print(" " * (n - i) + "*" * (2 * i - 1))


# ---------------------------------------------------------------
# 4. 2차원 리스트 다루기
# ---------------------------------------------------------------

# 리스트 안에 리스트를 넣으면 표(행렬)가 됩니다.
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

# 접근은 [행][열]
print(matrix[0][0])   # 1
print(matrix[1][2])   # 6
print(matrix[-1][-1]) # 9

# 전체 출력
print("\n[행렬 전체]")
for row in matrix:
    for value in row:
        print(f"{value:3d}", end="")
    print()

# 인덱스가 필요하면
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(f"({i},{j})={matrix[i][j]}", end=" ")
    print()

# 행 합계 / 열 합계
print("\n[행 합계]")
for i, row in enumerate(matrix):
    print(f"{i}행: {sum(row)}")

print("[열 합계]")
for j in range(len(matrix[0])):
    col_sum = 0
    for i in range(len(matrix)):
        col_sum += matrix[i][j]
    print(f"{j}열: {col_sum}")

# 전체 합계
total = 0
for row in matrix:
    total += sum(row)
print(f"전체 합계: {total}")


# ---------------------------------------------------------------
# 5. 2차원 리스트 만들기 - 흔한 함정
# ---------------------------------------------------------------

# [잘못된 방법] * 로 복사하면 같은 리스트를 가리키게 됩니다.
wrong = [[0] * 3] * 3
wrong[0][0] = 9
print(wrong)   # [[9,0,0],[9,0,0],[9,0,0]]  ← 전부 바뀜!

# [올바른 방법] 컴프리헨션으로 매번 새 리스트를 만듭니다.
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 9
print(grid)    # [[9,0,0],[0,0,0],[0,0,0]]


# ---------------------------------------------------------------
# 6. 조합 만들기
# ---------------------------------------------------------------

# 6-1. 메뉴 조합
coffees = ["아메리카노", "라떼"]
sizes = ["S", "M", "L"]

print("\n[가능한 주문 조합]")
for c in coffees:
    for s in sizes:
        print(f"{c} ({s})")

# 6-2. 두 주사위의 합이 7이 되는 경우
print("\n[주사위 합이 7]")
for a in range(1, 7):
    for b in range(1, 7):
        if a + b == 7:
            print(f"({a}, {b})", end=" ")
print()


# ---------------------------------------------------------------
# 7. 중첩 반복문에서 break
# ---------------------------------------------------------------

# break 는 '자기가 속한 반복문 하나'만 빠져나옵니다.
print("\n[안쪽만 break]")
for i in range(3):
    for j in range(3):
        if j == 1:
            break        # 안쪽 for 만 종료
        print(i, j)

# 바깥까지 한 번에 빠져나오려면 깃발(flag)을 씁니다.
print("\n[바깥까지 break]")
found = False
for i in range(3):
    for j in range(3):
        if i * j == 2:
            print(f"찾음: i={i}, j={j}")
            found = True
            break
    if found:
        break


# ---------------------------------------------------------------
# 8. 실전 예제 - 학생 × 과목 성적표
# ---------------------------------------------------------------

names = ["김철수", "이영희", "박민수"]
subjects = ["국어", "영어", "수학"]
scores = [
    [90, 85, 77],   # 김철수
    [88, 92, 95],   # 이영희
    [70, 65, 80],   # 박민수
]

print("\n" + "=" * 46)
print(f"{'이름':^8}", end="")
for sub in subjects:
    print(f"{sub:>8}", end="")
print(f"{'총점':>8}{'평균':>10}")
print("-" * 46)

for i, name in enumerate(names):
    print(f"{name:^8}", end="")
    for score in scores[i]:
        print(f"{score:>8}", end="")
    total = sum(scores[i])
    print(f"{total:>8}{total / len(subjects):>10.1f}")

print("-" * 46)

# 과목별 평균
print(f"{'과목평균':^8}", end="")
for j in range(len(subjects)):
    col_total = 0
    for i in range(len(names)):
        col_total += scores[i][j]
    print(f"{col_total / len(names):>8.1f}", end="")
print()
print("=" * 46)


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 1~5 사이 두 수의 모든 곱셈 결과를 표로 출력하세요.
#
# 2) 아래 모양을 출력하세요.
#    1
#    12
#    123
#    1234
#    12345
#
# 3) 3x3 행렬을 입력받아 전치행렬(행과 열을 바꾼 것)을 출력하세요.
#
# 4) 1~50 중 소수를 5개씩 줄바꿈하며 출력하세요.
