"""
4일차 - 03. 클래스 객체의 리스트 다루기

3일차에 '딕셔너리를 담은 리스트'를 다뤘습니다.
이번에는 '객체를 담은 리스트'를 다룹니다. 방법은 거의 같습니다.
차이는 s["name"] 대신 s.name 을 쓴다는 것뿐입니다.
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------
# 1. 클래스 정의
# ---------------------------------------------------------------

class Student:
    def __init__(self, name, major, scores):
        self.name = name
        self.major = major
        self.scores = scores

    def total(self):
        return sum(self.scores)

    def average(self):
        return sum(self.scores) / len(self.scores)

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"

    def is_passed(self):
        return self.average() >= 60 and all(s >= 40 for s in self.scores)

    def __str__(self):
        return f"{self.name}({self.major}) 평균 {self.average():.1f} {self.grade()}"

    def __repr__(self):
        return f"Student('{self.name}')"


# ---------------------------------------------------------------
# 2. 객체를 리스트에 담기
# ---------------------------------------------------------------

students = [
    Student("김철수", "ITM", [90, 85, 77]),
    Student("이영희", "ITM", [88, 92, 95]),
    Student("박민수", "산업공학", [70, 65, 80]),
    Student("최지우", "ITM", [100, 98, 96]),
    Student("정하늘", "산업공학", [55, 60, 72]),
]

print("[전체 목록]")
for s in students:
    print(f"  {s}")


# ---------------------------------------------------------------
# 3. 딕셔너리 방식과 비교
# ---------------------------------------------------------------
#
#  딕셔너리                          객체
#  -----------------------------    -----------------------------
#  s["name"]                        s.name
#  sum(s["scores"])/len(...)        s.average()
#  get_grade(get_average(s))        s.grade()
#
#  → 객체 쪽이 짧고, 오타를 편집기가 잡아 줍니다.


# ---------------------------------------------------------------
# 4. 정렬
# ---------------------------------------------------------------

print("\n[평균 높은 순]")
for rank, s in enumerate(sorted(students, key=lambda x: x.average(), reverse=True), 1):
    print(f"  {rank}등 {s.name:<8} {s.average():5.1f}")

print("\n[이름 가나다순]")
print("  ", [s.name for s in sorted(students, key=lambda x: x.name)])

print("\n[전공 → 평균 순 정렬]")
for s in sorted(students, key=lambda x: (x.major, -x.average())):
    print(f"  {s.major:<8} {s.name:<8} {s.average():.1f}")


# ---------------------------------------------------------------
# 5. 필터링
# ---------------------------------------------------------------

passed = [s for s in students if s.is_passed()]
print(f"\n합격: {[s.name for s in passed]}")

failed = [s for s in students if not s.is_passed()]
print(f"재시험: {[s.name for s in failed]}")

itm = [s for s in students if s.major == "ITM"]
print(f"ITM: {[s.name for s in itm]}")

a_grade = [s for s in students if s.grade() == "A"]
print(f"A학점: {[s.name for s in a_grade]}")


# ---------------------------------------------------------------
# 6. 집계
# ---------------------------------------------------------------

averages = [s.average() for s in students]
print(f"\n전체 평균: {sum(averages) / len(averages):.2f}")
print(f"최고: {max(students, key=lambda s: s.average()).name}")
print(f"최저: {min(students, key=lambda s: s.average()).name}")

grade_count = Counter(s.grade() for s in students)
print(f"학점 분포: {dict(grade_count)}")

by_major = defaultdict(list)
for s in students:
    by_major[s.major].append(s)

print("\n[전공별]")
for major, members in by_major.items():
    avg = sum(m.average() for m in members) / len(members)
    print(f"  {major}: {len(members)}명, 평균 {avg:.1f}")


# ---------------------------------------------------------------
# 7. 검색 - 찾는 함수를 만들어 두면 편합니다
# ---------------------------------------------------------------

def find_by_name(data, name):
    """이름이 정확히 일치하는 학생을 찾습니다. 없으면 None."""
    for s in data:
        if s.name == name:
            return s
    return None


def search(data, keyword):
    """이름에 keyword 가 들어간 학생을 모두 찾습니다."""
    return [s for s in data if keyword in s.name]


found = find_by_name(students, "이영희")
print(f"\n찾음: {found}")

print(f"'김' 검색: {[s.name for s in search(students, '김')]}")
print(f"'없음' 검색: {search(students, '없음')}")

# next() 를 쓰면 한 줄로도 됩니다. (없으면 두 번째 인자를 돌려줍니다)
found = next((s for s in students if s.name == "박민수"), None)
print(f"next 로 찾기: {found}")


# ---------------------------------------------------------------
# 8. 객체를 관리하는 클래스 만들기 - 한 단계 더
# ---------------------------------------------------------------

class StudentManager:
    """학생 목록을 관리하는 클래스."""

    def __init__(self):
        self.students = []

    def add(self, student):
        if self.find(student.name):
            print(f"'{student.name}' 은(는) 이미 있습니다.")
            return False
        self.students.append(student)
        return True

    def remove(self, name):
        target = self.find(name)
        if target is None:
            return False
        self.students.remove(target)
        return True

    def find(self, name):
        for s in self.students:
            if s.name == name:
                return s
        return None

    def ranked(self):
        return sorted(self.students, key=lambda s: s.average(), reverse=True)

    def average(self):
        if not self.students:
            return 0.0
        return sum(s.average() for s in self.students) / len(self.students)

    def report(self):
        print("\n" + "=" * 50)
        print(f" 전체 {len(self.students)}명 / 평균 {self.average():.2f}점")
        print("=" * 50)
        for rank, s in enumerate(self.ranked(), start=1):
            mark = "✓" if s.is_passed() else "✗"
            print(f" {rank}등  {mark} {s.name:<8} {s.average():5.1f}  {s.grade()}")
        print("=" * 50)

    def __len__(self):
        """len(manager) 로 인원수를 셀 수 있게 합니다."""
        return len(self.students)

    def __iter__(self):
        """for s in manager: 가 가능하게 합니다."""
        return iter(self.students)


manager = StudentManager()
for s in students:
    manager.add(s)

manager.add(Student("김철수", "ITM", [50, 50, 50]))    # 중복 → 거부됨

manager.report()

print(f"\nlen(manager) = {len(manager)}")
print("for 로 순회:", [s.name for s in manager])

manager.remove("정하늘")
print(f"삭제 후 인원: {len(manager)}명")


# ===============================================================
# 연습 문제
# ===============================================================
# 1) StudentManager 에 '과목별 1등 찾기' 메서드를 추가하세요.
#
# 2) Product 클래스와 Inventory(재고 관리) 클래스를 만드세요.
#    입고/출고/재고조회/총재고금액 기능을 넣으세요.
#
# 3) StudentManager 에 __getitem__ 을 구현해
#    manager[0] 으로 접근할 수 있게 만드세요.
#
# 4) 성적을 수정하는 메서드를 만들고, 수정 이력을 남기게 하세요.
