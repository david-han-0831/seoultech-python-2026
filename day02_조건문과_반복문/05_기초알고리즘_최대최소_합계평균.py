"""
2일차 - 05. 기초 알고리즘 (최대/최소, 합계/평균, 개수 세기)

max(), sum() 같은 내장 함수를 쓰면 한 줄이지만,
'어떻게 그렇게 되는지'를 직접 구현해 보는 것이 알고리즘 학습의 출발점입니다.
"""

data = [64, 25, 12, 90, 11, 78, 33, 90, 47]

print(f"데이터: {data}")
print(f"개수  : {len(data)}")
print()


# ---------------------------------------------------------------
# 1. 합계 - 내장 함수 없이
# ---------------------------------------------------------------

total = 0                 # ① 그릇을 0으로 준비
for value in data:        # ② 하나씩 꺼내서
    total += value        # ③ 계속 더한다
print(f"합계(직접): {total}")
print(f"합계(내장): {sum(data)}")


# ---------------------------------------------------------------
# 2. 평균
# ---------------------------------------------------------------

average = total / len(data)
print(f"평균: {average:.2f}")

# [주의] 빈 리스트면 0으로 나누게 되어 에러가 납니다.
empty = []
if len(empty) > 0:
    print(sum(empty) / len(empty))
else:
    print("평균: 데이터가 없습니다.")


# ---------------------------------------------------------------
# 3. 최댓값 - 직접 구하기
# ---------------------------------------------------------------

# 핵심 아이디어: 첫 값을 '임시 1등'으로 두고, 더 큰 걸 만나면 교체한다.
max_value = data[0]
for value in data:
    if value > max_value:
        max_value = value
print(f"\n최댓값(직접): {max_value}")
print(f"최댓값(내장): {max(data)}")

# [흔한 실수] max_value = 0 으로 시작하면 안 됩니다.
#             음수만 들어 있는 데이터에서 답이 틀립니다.
negatives = [-5, -2, -9]
wrong = 0
for v in negatives:
    if v > wrong:
        wrong = v
print(f"잘못된 방법: {wrong} (정답은 {max(negatives)})")


# ---------------------------------------------------------------
# 4. 최솟값
# ---------------------------------------------------------------

min_value = data[0]
for value in data:
    if value < min_value:
        min_value = value
print(f"\n최솟값(직접): {min_value}")
print(f"최솟값(내장): {min(data)}")


# ---------------------------------------------------------------
# 5. 최댓값의 '위치' 찾기
# ---------------------------------------------------------------

max_index = 0
for i in range(len(data)):
    if data[i] > data[max_index]:
        max_index = i
print(f"\n최댓값 {data[max_index]} 은(는) {max_index}번 자리에 있습니다.")
print(f"내장 함수 index(): {data.index(max(data))}")

# 최댓값이 여러 개일 때 모든 위치 찾기
max_value = max(data)
positions = []
for i, v in enumerate(data):
    if v == max_value:
        positions.append(i)
print(f"최댓값이 있는 모든 위치: {positions}")


# ---------------------------------------------------------------
# 6. 개수 세기 (조건에 맞는 것)
# ---------------------------------------------------------------

count_over_50 = 0
for value in data:
    if value > 50:
        count_over_50 += 1
print(f"\n50 초과: {count_over_50}개")

# 한 줄로 (컴프리헨션 + sum)
print(f"50 초과: {sum(1 for v in data if v > 50)}개")
print(f"50 초과: {len([v for v in data if v > 50])}개")


# ---------------------------------------------------------------
# 7. 두 번째로 큰 값 찾기
# ---------------------------------------------------------------

# 방법 1: 정렬 후 뒤에서 두 번째 (중복 제거 필요)
unique_sorted = sorted(set(data), reverse=True)
print(f"\n두 번째로 큰 값: {unique_sorted[1]}")

# 방법 2: 한 번만 훑으면서 1등·2등을 동시에 관리 (더 효율적)
first = second = float("-inf")   # 아주 작은 값으로 시작
for v in data:
    if v > first:
        second = first
        first = v
    elif first > v > second:
        second = v
print(f"두 번째로 큰 값(직접): {second}")


# ---------------------------------------------------------------
# 8. 실전 예제 - 성적 통계
# ---------------------------------------------------------------

scores = {
    "김철수": 88,
    "이영희": 95,
    "박민수": 70,
    "최지우": 100,
    "정하늘": 62,
}

total = sum(scores.values())
average = total / len(scores)

print("\n" + "=" * 34)
print(" 성적 통계")
print("=" * 34)
print(f"인원   : {len(scores)}명")
print(f"총점   : {total}점")
print(f"평균   : {average:.2f}점")
print(f"최고점 : {max(scores.values())}점")
print(f"최저점 : {min(scores.values())}점")

# 최고점 학생 이름까지
top_name = max(scores, key=scores.get)
print(f"1등    : {top_name}")

# 평균 이상 / 미만
above = []
below = []
for name, score in scores.items():
    if score >= average:
        above.append(name)
    else:
        below.append(name)

print(f"\n평균 이상({len(above)}명): {', '.join(above)}")
print(f"평균 미만({len(below)}명): {', '.join(below)}")

# 편차 (각자 평균에서 얼마나 떨어져 있는지)
print("\n[평균 대비 편차]")
for name, score in scores.items():
    diff = score - average
    sign = "+" if diff >= 0 else ""
    print(f"  {name}: {score}점 ({sign}{diff:.1f})")


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 숫자 리스트에서 짝수의 합과 홀수의 합을 각각 구하세요.
#
# 2) 리스트에서 두 번째로 작은 값을 내장 함수 없이 구하세요.
#
# 3) 문자열 리스트에서 가장 긴 문자열을 찾으세요.
#    words = ["python", "is", "awesome", "language"]
#
# 4) 온도 데이터에서 전날보다 오른 날이 며칠인지 세어 보세요.
#    temps = [21, 23, 22, 25, 27, 26, 28]
