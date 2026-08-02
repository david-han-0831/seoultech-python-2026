"""
2일차 실습 - 업다운 숫자 맞추기 게임

오늘 배운 것을 모두 씁니다.
  while / if / break / continue / 함수 / 리스트

컴퓨터가 정한 숫자를 맞히는 게임입니다.
"""

import random


# ---------------------------------------------------------------
# 함수들
# ---------------------------------------------------------------

def choose_difficulty():
    """난이도를 골라 (최댓값, 기회 횟수) 를 돌려줍니다."""
    print("\n난이도를 선택하세요.")
    print("  1. 쉬움   (1~50,  기회 8번)")
    print("  2. 보통   (1~100, 기회 7번)")
    print("  3. 어려움 (1~500, 기회 9번)")

    while True:
        choice = input("선택: ").strip()
        if choice == "1":
            return 50, 8
        elif choice == "2":
            return 100, 7
        elif choice == "3":
            return 500, 9
        else:
            print("1, 2, 3 중에서 선택해 주세요.")


def get_guess(max_number):
    """올바른 숫자를 입력할 때까지 반복해서 물어봅니다."""
    while True:
        raw = input("추측한 숫자: ").strip()

        if not raw.isdigit():
            print("  숫자만 입력해 주세요.")
            continue

        guess = int(raw)
        if not (1 <= guess <= max_number):
            print(f"  1 ~ {max_number} 사이로 입력해 주세요.")
            continue

        return guess


def give_hint(guess, answer):
    """정답보다 큰지 작은지 알려줍니다."""
    gap = abs(guess - answer)

    if guess < answer:
        direction = "UP ↑  (더 큰 수)"
    else:
        direction = "DOWN ↓ (더 작은 수)"

    # 얼마나 가까운지도 알려 줍니다.
    if gap <= 3:
        closeness = "🔥 아주 가까워요!"
    elif gap <= 10:
        closeness = "😊 가까워요"
    else:
        closeness = "🥶 멀어요"

    print(f"  {direction}   {closeness}")


def play_one_game():
    """게임 한 판을 진행하고 (성공여부, 사용한 횟수) 를 돌려줍니다."""
    max_number, max_tries = choose_difficulty()
    answer = random.randint(1, max_number)

    print(f"\n1 ~ {max_number} 사이의 숫자를 맞혀 보세요. 기회는 {max_tries}번입니다.")
    print("-" * 44)

    history = []   # 지금까지 입력한 숫자들

    for attempt in range(1, max_tries + 1):
        print(f"\n[{attempt}/{max_tries}번째 시도]", end="  ")
        if history:
            print(f"지금까지: {history}")
        else:
            print()

        guess = get_guess(max_number)

        if guess in history:
            print("  이미 입력한 숫자입니다. (기회는 그대로 둘게요)")
            continue

        history.append(guess)

        if guess == answer:
            print(f"\n🎉 정답입니다! {attempt}번 만에 맞히셨습니다.")
            return True, attempt

        give_hint(guess, answer)

    print(f"\n💀 기회를 모두 사용했습니다. 정답은 {answer} 였습니다.")
    return False, max_tries


# ---------------------------------------------------------------
# 메인 - 여러 판을 이어서 진행하고 전적을 남깁니다
# ---------------------------------------------------------------

print("=" * 44)
print(" 업다운 숫자 맞추기 게임")
print("=" * 44)

win_count = 0
lose_count = 0
records = []      # 성공한 판의 시도 횟수를 모아둡니다

while True:
    success, tries = play_one_game()

    if success:
        win_count += 1
        records.append(tries)
    else:
        lose_count += 1

    # 전적 출력
    print("\n" + "-" * 44)
    print(f"전적: {win_count}승 {lose_count}패", end="")
    if records:
        print(f"  |  평균 {sum(records) / len(records):.1f}번 만에 성공"
              f"  |  최고 기록 {min(records)}번")
    else:
        print()
    print("-" * 44)

    again = input("\n한 판 더 하시겠습니까? (y/n): ").strip().lower()
    if again != "y":
        break

print("\n게임을 종료합니다. 수고하셨습니다!")


# ===============================================================
# 더 해보기
# ===============================================================
# 1) 반대로 '사람이 정한 숫자를 컴퓨터가 맞히는' 모드를 만들어 보세요.
#    힌트: 컴퓨터는 범위의 가운데를 찍으면 됩니다 (이진 탐색)
#
# 2) 점수 제도를 넣어 보세요.
#    (남은 기회 × 난이도 배수)
#
# 3) 4일차에 배울 파일 입출력을 붙여 최고 기록을 저장해 보세요.
