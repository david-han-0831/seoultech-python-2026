"""성적 계산과 관련된 함수들을 모아 둔 모듈."""

PASS_CUTOFF = 60        # 합격 기준 평균
MIN_SCORE = 40          # 과목별 최저 점수


def get_average(scores):
    """점수 목록의 평균을 돌려줍니다. 비어 있으면 0."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def to_grade(average):
    """평균 점수를 학점으로 바꿉니다."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def is_passed(scores, cutoff=PASS_CUTOFF, min_score=MIN_SCORE):
    """합격 여부를 판정합니다.

    평균이 cutoff 이상이고 모든 과목이 min_score 이상이어야 합격입니다.
    """
    if get_average(scores) < cutoff:
        return False
    return all(s >= min_score for s in scores)


def rank_of(target, all_scores):
    """전체 점수 목록에서 target 이 몇 등인지 돌려줍니다."""
    higher = sum(1 for s in all_scores if s > target)
    return higher + 1


# 이 파일을 직접 실행했을 때만 아래가 돌아갑니다.
# 다른 파일에서 import 할 때는 실행되지 않습니다.
if __name__ == "__main__":
    print("[score.py 자체 테스트]")
    print(get_average([90, 85, 77]))
    print(to_grade(84.0))
    print(is_passed([90, 85, 77]))
    print(is_passed([90, 85, 30]))     # 한 과목이 40점 미만 → False
    print(rank_of(85, [90, 85, 77, 95]))
