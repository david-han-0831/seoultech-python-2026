"""
3일차 실습 - 학생 성적 관리 프로그램 (함수 버전)

1일차에 만든 '학생 정보 출력기'를 함수로 정리하고 기능을 확장합니다.
4일차에 이 프로그램을 클래스로 다시 만들고, 파일 저장까지 붙일 예정입니다.

사용 문법: 함수 / 딕셔너리 / 리스트 / 컴프리헨션 / lambda / Counter
"""

from collections import Counter, defaultdict

# ---------------------------------------------------------------
# 데이터 - 시작할 때 들어 있는 샘플
# ---------------------------------------------------------------

SUBJECTS = ["국어", "영어", "수학"]

students = [
    {"name": "김철수", "major": "ITM", "scores": [90, 85, 77]},
    {"name": "이영희", "major": "ITM", "scores": [88, 92, 95]},
    {"name": "박민수", "major": "산업공학", "scores": [70, 65, 80]},
    {"name": "최지우", "major": "ITM", "scores": [100, 98, 96]},
    {"name": "정하늘", "major": "산업공학", "scores": [55, 60, 72]},
]


# ---------------------------------------------------------------
# 계산 함수 - 값만 돌려주고 출력은 하지 않습니다
# ---------------------------------------------------------------

def get_total(student):
    """총점을 돌려줍니다."""
    return sum(student["scores"])


def get_average(student):
    """평균을 돌려줍니다."""
    return sum(student["scores"]) / len(student["scores"])


def get_grade(average):
    """평균 점수로 학점을 매깁니다."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def is_passed(student, cutoff=60, min_score=40):
    """합격 여부를 판정합니다.

    평균이 cutoff 이상이고, 모든 과목이 min_score 이상이어야 합격입니다.
    """
    if get_average(student) < cutoff:
        return False
    return all(score >= min_score for score in student["scores"])


def get_ranked(data):
    """평균 내림차순으로 정렬한 새 리스트를 돌려줍니다."""
    return sorted(data, key=get_average, reverse=True)


def get_subject_averages(data):
    """과목별 평균을 딕셔너리로 돌려줍니다."""
    result = {}
    for i, subject in enumerate(SUBJECTS):
        scores = [s["scores"][i] for s in data]
        result[subject] = sum(scores) / len(scores)
    return result


def group_by_major(data):
    """전공별로 학생을 묶습니다."""
    grouped = defaultdict(list)
    for s in data:
        grouped[s["major"]].append(s)
    return dict(grouped)


# ---------------------------------------------------------------
# 출력 함수 - 화면에 보여주는 일만 합니다
# ---------------------------------------------------------------

def print_header(title):
    """구분선이 있는 제목을 출력합니다."""
    print()
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_table(data):
    """성적표를 표로 출력합니다."""
    if not data:
        print("등록된 학생이 없습니다.")
        return

    header = f"{'이름':^8}{'전공':^10}"
    for subject in SUBJECTS:
        header += f"{subject:>6}"
    header += f"{'총점':>7}{'평균':>8}{'학점':>6}{'판정':>8}"
    print(header)
    print("-" * 60)

    for s in data:
        avg = get_average(s)
        row = f"{s['name']:^8}{s['major']:^10}"
        for score in s["scores"]:
            row += f"{score:>6}"
        row += f"{get_total(s):>7}{avg:>8.1f}{get_grade(avg):>6}"
        row += f"{'합격' if is_passed(s) else '재시험':>8}"
        print(row)

    print("-" * 60)


def print_statistics(data):
    """전체 통계를 출력합니다."""
    if not data:
        return

    averages = [get_average(s) for s in data]
    overall = sum(averages) / len(averages)

    print(f"\n인원      : {len(data)}명")
    print(f"전체 평균 : {overall:.2f}점")
    print(f"최고 평균 : {max(averages):.1f}점")
    print(f"최저 평균 : {min(averages):.1f}점")

    print("\n[과목별 평균]")
    for subject, avg in get_subject_averages(data).items():
        bar = "█" * int(avg / 5)          # 5점당 한 칸
        print(f"  {subject} {avg:5.1f}  {bar}")

    print("\n[학점 분포]")
    grades = Counter(get_grade(get_average(s)) for s in data)
    for grade in ["A", "B", "C", "D", "F"]:
        count = grades.get(grade, 0)
        if count:
            print(f"  {grade}학점: {'●' * count} {count}명")

    passed = [s for s in data if is_passed(s)]
    rate = len(passed) / len(data) * 100
    print(f"\n합격률: {len(passed)}/{len(data)}명 ({rate:.1f}%)")


def print_ranking(data, top=None):
    """석차를 출력합니다. top 을 주면 상위 몇 명만 봅니다."""
    ranked = get_ranked(data)
    if top:
        ranked = ranked[:top]

    print("\n[석차]")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for rank, s in enumerate(ranked, start=1):
        medal = medals.get(rank, "  ")
        avg = get_average(s)
        print(f"  {medal} {rank}등  {s['name']:<8} {avg:5.1f}점 ({get_grade(avg)})")


def print_by_major(data):
    """전공별 현황을 출력합니다."""
    print("\n[전공별 현황]")
    grouped = group_by_major(data)

    # 전공 평균이 높은 순으로 보여줍니다.
    def major_average(item):
        _, members = item
        return sum(get_average(s) for s in members) / len(members)

    for major, members in sorted(grouped.items(), key=major_average, reverse=True):
        avg = sum(get_average(s) for s in members) / len(members)
        names = ", ".join(s["name"] for s in members)
        print(f"  {major:<10} {len(members)}명  평균 {avg:.1f}점")
        print(f"    → {names}")


# ---------------------------------------------------------------
# 기능 함수
# ---------------------------------------------------------------

def add_student(data):
    """새 학생을 추가합니다."""
    name = input("이름: ").strip()

    if any(s["name"] == name for s in data):
        print(f"'{name}' 은(는) 이미 등록되어 있습니다.")
        return

    major = input("전공: ").strip()

    scores = []
    for subject in SUBJECTS:
        while True:
            raw = input(f"{subject} 점수(0~100): ").strip()
            if raw.isdigit() and 0 <= int(raw) <= 100:
                scores.append(int(raw))
                break
            print("  0~100 사이의 숫자를 입력해 주세요.")

    data.append({"name": name, "major": major, "scores": scores})
    print(f"'{name}' 을(를) 추가했습니다.")


def search_student(data):
    """이름으로 학생을 검색합니다."""
    keyword = input("검색할 이름: ").strip()
    found = [s for s in data if keyword in s["name"]]

    if not found:
        print(f"'{keyword}' 에 해당하는 학생이 없습니다.")
        return

    print(f"\n{len(found)}명을 찾았습니다.")
    print_table(found)

    # 전체에서 몇 등인지도 알려 줍니다.
    ranked = get_ranked(data)
    for s in found:
        rank = ranked.index(s) + 1
        print(f"  {s['name']}: 전체 {len(data)}명 중 {rank}등")


def delete_student(data):
    """학생을 삭제합니다."""
    name = input("삭제할 이름: ").strip()

    target = None
    for s in data:
        if s["name"] == name:
            target = s
            break

    if target is None:
        print(f"'{name}' 을(를) 찾을 수 없습니다.")
        return

    if input(f"'{name}' 을(를) 삭제할까요? (y/n): ").strip().lower() == "y":
        data.remove(target)
        print("삭제했습니다.")
    else:
        print("취소했습니다.")


# ---------------------------------------------------------------
# 메인 메뉴
# ---------------------------------------------------------------

def show_menu():
    print("\n" + "-" * 36)
    print(" 1. 전체 성적표      2. 통계")
    print(" 3. 석차            4. 전공별 현황")
    print(" 5. 학생 추가       6. 검색")
    print(" 7. 삭제            0. 종료")
    print("-" * 36)


def main():
    print_header("학생 성적 관리 프로그램")

    while True:
        show_menu()
        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            print_header("전체 성적표")
            print_table(get_ranked(students))
        elif choice == "2":
            print_header("통계")
            print_statistics(students)
        elif choice == "3":
            print_header("석차")
            print_ranking(students)
        elif choice == "4":
            print_header("전공별 현황")
            print_by_major(students)
        elif choice == "5":
            add_student(students)
        elif choice == "6":
            search_student(students)
        elif choice == "7":
            delete_student(students)
        elif choice == "0":
            print("\n프로그램을 종료합니다.")
            break
        else:
            print("0~7 중에서 선택해 주세요.")


# 이 파일을 직접 실행했을 때만 main() 이 돌아갑니다.
# 다른 파일에서 import 하면 실행되지 않습니다. (4일차 '모듈'에서 다룹니다)
if __name__ == "__main__":
    main()


# ===============================================================
# 더 해보기
# ===============================================================
# 1) 과목을 추가·삭제할 수 있게 만들어 보세요. (SUBJECTS 를 바꾸면?)
# 2) 성적 수정 기능을 추가하세요.
# 3) 과목별 1등을 각각 찾아 출력하세요.
# 4) 4일차 파일 입출력을 붙여 프로그램을 껐다 켜도 데이터가 남게 하세요.
