"""
4일차 실습 - 학생 성적 관리 프로그램 (클래스 + 파일 저장 버전)

3일차에 함수로 만든 프로그램을 클래스로 다시 만들고,
JSON·CSV 저장 기능을 붙여 '껐다 켜도 데이터가 남는' 프로그램으로 완성합니다.

사용 문법: 클래스 / 상속 / 예외처리 / 파일 입출력 / JSON / CSV / 모듈
"""

import csv
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

# 4일차에 만든 패키지를 가져다 씁니다.
from mytools import to_grade, make_line

DATA_DIR = "output"
DATA_PATH = os.path.join(DATA_DIR, "students.json")
CSV_PATH = os.path.join(DATA_DIR, "students_report.csv")

SUBJECTS = ["국어", "영어", "수학"]

os.makedirs(DATA_DIR, exist_ok=True)


# ===============================================================
# 예외 클래스
# ===============================================================

class StudentError(Exception):
    """이 프로그램에서 쓰는 예외들의 부모."""


class DuplicateStudentError(StudentError):
    def __init__(self, name):
        super().__init__(f"'{name}' 학생은 이미 등록되어 있습니다.")


class StudentNotFoundError(StudentError):
    def __init__(self, name):
        super().__init__(f"'{name}' 학생을 찾을 수 없습니다.")


class InvalidScoreError(StudentError):
    def __init__(self, score):
        super().__init__(f"점수는 0~100 사이여야 합니다. (입력값: {score})")


# ===============================================================
# 모델 클래스
# ===============================================================

class Student:
    """학생 한 명."""

    def __init__(self, name, major, scores=None):
        if not name.strip():
            raise ValueError("이름을 입력해 주세요.")

        self.name = name.strip()
        self.major = major.strip() or "미지정"
        self.scores = []

        for score in (scores or []):
            self.add_score(score)

    # ---- 계산 ---------------------------------------------------

    def add_score(self, score):
        if not isinstance(score, int) or not (0 <= score <= 100):
            raise InvalidScoreError(score)
        self.scores.append(score)

    def total(self):
        return sum(self.scores)

    def average(self):
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def grade(self):
        return to_grade(self.average())     # mytools 에서 가져온 함수

    def is_passed(self, cutoff=60, min_score=40):
        if self.average() < cutoff:
            return False
        return all(s >= min_score for s in self.scores)

    # ---- 저장/복원 ----------------------------------------------

    def to_dict(self):
        return {"name": self.name, "major": self.major, "scores": self.scores}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["major"], data.get("scores", []))

    # ---- 표현 ---------------------------------------------------

    def __str__(self):
        return f"{self.name}({self.major}) 평균 {self.average():.1f} {self.grade()}"

    def __repr__(self):
        return f"Student('{self.name}')"


class GraduateStudent(Student):
    """대학원생 - 지도교수와 논문 정보가 추가됩니다."""

    def __init__(self, name, major, scores=None, advisor="미정"):
        super().__init__(name, major, scores)
        self.advisor = advisor
        self.thesis_submitted = False

    def submit_thesis(self):
        self.thesis_submitted = True

    def is_passed(self, cutoff=70, min_score=50):
        """대학원생은 기준이 더 높고 논문도 내야 합니다."""
        return super().is_passed(cutoff, min_score) and self.thesis_submitted

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "graduate"
        data["advisor"] = self.advisor
        data["thesis_submitted"] = self.thesis_submitted
        return data

    def __str__(self):
        mark = "논문제출" if self.thesis_submitted else "논문미제출"
        return f"{super().__str__()} [{self.advisor} 지도 / {mark}]"


# ===============================================================
# 관리 클래스
# ===============================================================

class StudentManager:
    """학생 목록을 관리하고 파일에 저장합니다."""

    def __init__(self, filepath=DATA_PATH):
        self.filepath = filepath
        self.students = []

    # ---- CRUD ---------------------------------------------------

    def add(self, student):
        if self.find(student.name):
            raise DuplicateStudentError(student.name)
        self.students.append(student)

    def remove(self, name):
        target = self.find(name)
        if target is None:
            raise StudentNotFoundError(name)
        self.students.remove(target)
        return target

    def find(self, name):
        for s in self.students:
            if s.name == name:
                return s
        return None

    def search(self, keyword):
        return [s for s in self.students if keyword in s.name]

    # ---- 조회 ---------------------------------------------------

    def ranked(self):
        return sorted(self.students, key=lambda s: s.average(), reverse=True)

    def rank_of(self, name):
        target = self.find(name)
        if target is None:
            raise StudentNotFoundError(name)
        return self.ranked().index(target) + 1

    def class_average(self):
        if not self.students:
            return 0.0
        return sum(s.average() for s in self.students) / len(self.students)

    def subject_averages(self):
        result = {}
        for i, subject in enumerate(SUBJECTS):
            values = [s.scores[i] for s in self.students if len(s.scores) > i]
            result[subject] = sum(values) / len(values) if values else 0.0
        return result

    def by_major(self):
        grouped = defaultdict(list)
        for s in self.students:
            grouped[s.major].append(s)
        return dict(grouped)

    # ---- 파일 ---------------------------------------------------

    def save(self):
        """JSON 으로 저장합니다."""
        payload = {
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "subjects": SUBJECTS,
            "students": [s.to_dict() for s in self.students],
        }
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return len(self.students)

    def load(self):
        """JSON 에서 불러옵니다. 파일이 없으면 조용히 넘어갑니다."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except FileNotFoundError:
            return 0
        except json.JSONDecodeError as e:
            print(f"[경고] 저장 파일이 손상되었습니다: {e}")
            return 0

        self.students = []
        for data in payload.get("students", []):
            try:
                if data.get("type") == "graduate":
                    s = GraduateStudent(
                        data["name"], data["major"], data.get("scores", []),
                        data.get("advisor", "미정"),
                    )
                    s.thesis_submitted = data.get("thesis_submitted", False)
                else:
                    s = Student.from_dict(data)
                self.students.append(s)
            except (KeyError, ValueError, InvalidScoreError) as e:
                print(f"[경고] 잘못된 데이터를 건너뜁니다: {e}")

        return len(self.students)

    def export_csv(self, filepath=CSV_PATH):
        """엑셀에서 열 수 있는 CSV 로 내보냅니다."""
        if not self.students:
            raise StudentError("내보낼 데이터가 없습니다.")

        fieldnames = ["순위", "이름", "전공"] + SUBJECTS + ["총점", "평균", "학점", "판정"]

        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for rank, s in enumerate(self.ranked(), start=1):
                row = {
                    "순위": rank,
                    "이름": s.name,
                    "전공": s.major,
                    "총점": s.total(),
                    "평균": round(s.average(), 1),
                    "학점": s.grade(),
                    "판정": "합격" if s.is_passed() else "재시험",
                }
                for i, subject in enumerate(SUBJECTS):
                    row[subject] = s.scores[i] if len(s.scores) > i else ""
                writer.writerow(row)

        return filepath

    # ---- 출력 ---------------------------------------------------

    def print_table(self):
        if not self.students:
            print("등록된 학생이 없습니다.")
            return

        print(make_line("=", 66))
        header = f"{'순위':^5}{'이름':^9}{'전공':^11}"
        for subject in SUBJECTS:
            header += f"{subject:>6}"
        header += f"{'총점':>7}{'평균':>8}{'학점':>5}"
        print(header)
        print(make_line("-", 66))

        for rank, s in enumerate(self.ranked(), start=1):
            row = f"{rank:^5}{s.name:^9}{s.major:^11}"
            for i in range(len(SUBJECTS)):
                row += f"{s.scores[i] if len(s.scores) > i else '-':>6}"
            row += f"{s.total():>7}{s.average():>8.1f}{s.grade():>5}"
            print(row)

        print(make_line("=", 66))

    def print_statistics(self):
        if not self.students:
            print("등록된 학생이 없습니다.")
            return

        print(f"\n인원      : {len(self.students)}명")
        print(f"전체 평균 : {self.class_average():.2f}점")

        print("\n[과목별 평균]")
        for subject, avg in self.subject_averages().items():
            print(f"  {subject} {avg:5.1f}  {'█' * int(avg / 5)}")

        print("\n[학점 분포]")
        grades = Counter(s.grade() for s in self.students)
        for grade in ["A", "B", "C", "D", "F"]:
            if grades.get(grade):
                print(f"  {grade}: {'●' * grades[grade]} {grades[grade]}명")

        print("\n[전공별]")
        for major, members in self.by_major().items():
            avg = sum(m.average() for m in members) / len(members)
            print(f"  {major:<10} {len(members)}명, 평균 {avg:.1f}점")

        passed = [s for s in self.students if s.is_passed()]
        print(f"\n합격률: {len(passed)}/{len(self.students)}명 "
              f"({len(passed) / len(self.students) * 100:.1f}%)")

    def __len__(self):
        return len(self.students)

    def __iter__(self):
        return iter(self.students)


# ===============================================================
# 입력 도우미
# ===============================================================

def input_int(prompt, min_value=0, max_value=100):
    """정수를 안전하게 입력받습니다."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  숫자를 입력해 주세요.")
            continue
        if not (min_value <= value <= max_value):
            print(f"  {min_value}~{max_value} 사이로 입력해 주세요.")
            continue
        return value


# ===============================================================
# 메뉴 동작
# ===============================================================

def action_add(manager):
    name = input("이름: ").strip()
    major = input("전공: ").strip()

    scores = [input_int(f"{subject} 점수: ") for subject in SUBJECTS]

    is_grad = input("대학원생입니까? (y/n): ").strip().lower() == "y"

    try:
        if is_grad:
            advisor = input("지도교수: ").strip() or "미정"
            student = GraduateStudent(name, major, scores, advisor)
            if input("논문을 제출했습니까? (y/n): ").strip().lower() == "y":
                student.submit_thesis()
        else:
            student = Student(name, major, scores)

        manager.add(student)
        manager.save()
        print(f"등록 완료: {student}")

    except (StudentError, ValueError) as e:
        print(f"등록 실패: {e}")


def action_search(manager):
    keyword = input("검색어(이름 일부): ").strip()
    found = manager.search(keyword)

    if not found:
        print(f"'{keyword}' 에 해당하는 학생이 없습니다.")
        return

    print(f"\n{len(found)}명을 찾았습니다.")
    for s in found:
        print(f"  {s}")
        print(f"    총점 {s.total()}점 / 전체 {len(manager)}명 중 "
              f"{manager.rank_of(s.name)}등 / "
              f"{'합격' if s.is_passed() else '재시험'}")


def action_delete(manager):
    name = input("삭제할 이름: ").strip()
    try:
        target = manager.find(name)
        if target is None:
            raise StudentNotFoundError(name)

        print(f"  대상: {target}")
        if input("  정말 삭제할까요? (y/n): ").strip().lower() != "y":
            print("  취소했습니다.")
            return

        manager.remove(name)
        manager.save()
        print("  삭제했습니다.")

    except StudentError as e:
        print(f"삭제 실패: {e}")


def action_export(manager):
    try:
        path = manager.export_csv()
        print(f"CSV 로 내보냈습니다: {path}")
        print("(엑셀에서 바로 열립니다)")
    except StudentError as e:
        print(f"내보내기 실패: {e}")


# ===============================================================
# 메인
# ===============================================================

def make_sample_data(manager):
    """처음 실행했을 때 넣어 둘 샘플 데이터."""
    samples = [
        Student("김철수", "ITM", [90, 85, 77]),
        Student("이영희", "ITM", [88, 92, 95]),
        Student("박민수", "산업공학", [70, 65, 80]),
        Student("최지우", "ITM", [100, 98, 96]),
        Student("정하늘", "산업공학", [55, 60, 72]),
        GraduateStudent("한동윤", "ITM", [95, 90, 88], "홍길동"),
    ]
    for s in samples:
        manager.add(s)
    manager.save()


def show_menu():
    print("\n" + make_line("-", 40))
    print(" 1. 성적표      2. 통계        3. 검색")
    print(" 4. 학생 추가   5. 삭제        6. CSV 내보내기")
    print(" 0. 종료")
    print(make_line("-", 40))


def main():
    manager = StudentManager()
    loaded = manager.load()

    print(make_line("=", 66))
    print(" 학생 성적 관리 프로그램 v2.0 (클래스 + 파일 저장)")
    print(make_line("=", 66))

    if loaded:
        print(f"저장된 데이터 {loaded}명을 불러왔습니다.")
    else:
        print("저장된 데이터가 없어 샘플을 생성합니다.")
        make_sample_data(manager)

    while True:
        show_menu()
        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            manager.print_table()
        elif choice == "2":
            manager.print_statistics()
        elif choice == "3":
            action_search(manager)
        elif choice == "4":
            action_add(manager)
        elif choice == "5":
            action_delete(manager)
        elif choice == "6":
            action_export(manager)
        elif choice == "0":
            count = manager.save()
            print(f"\n{count}명의 데이터를 저장하고 종료합니다.")
            break
        else:
            print("0~6 중에서 선택해 주세요.")


if __name__ == "__main__":
    main()


# ===============================================================
# 더 해보기
# ===============================================================
# 1) 성적 수정 메뉴를 추가하고, 수정 이력을 파일에 남기세요.
# 2) 과목을 프로그램 안에서 추가·삭제할 수 있게 만드세요.
# 3) CSV 를 '불러오는' 기능도 만드세요. (지금은 내보내기만 됩니다)
# 4) 파일을 models.py / storage.py / views.py / main.py 로 나눠 보세요.
# 5) 2주차에 배울 matplotlib 으로 성적 그래프를 그려 보세요.
