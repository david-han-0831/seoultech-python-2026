"""
1일차 실습 ① - 학생 정보 출력기

오늘 배운 것을 모아 만듭니다.
  변수 / input / 형변환 / f-string / 리스트 / 딕셔너리

여러 명의 정보를 입력받아 표 형태로 정리해 출력합니다.
"""

# ---------------------------------------------------------------
# 1. 몇 명을 입력할지 먼저 물어봅니다
# ---------------------------------------------------------------

print("=" * 46)
print(" 학생 정보 출력기")
print("=" * 46)

count = int(input("몇 명을 입력하시겠습니까? "))

# 입력받은 학생들을 담아둘 빈 리스트
students = []


# ---------------------------------------------------------------
# 2. 사람 수만큼 반복하며 입력받습니다
#    (for 문은 2일차에 자세히 배우지만 여기서는 '반복'만 이해하면 됩니다)
# ---------------------------------------------------------------

for i in range(count):
    print(f"\n--- {i + 1}번째 학생 ---")

    name = input("이름: ").strip()
    student_id = input("학번: ").strip()
    major = input("전공: ").strip()

    # 점수 세 개를 한 줄에 공백으로 받습니다.
    kor, eng, math = map(int, input("국어 영어 수학 점수: ").split())

    total = kor + eng + math
    average = total / 3

    # 학생 한 명의 정보를 딕셔너리 하나로 묶습니다.
    student = {
        "name": name,
        "id": student_id,
        "major": major,
        "kor": kor,
        "eng": eng,
        "math": math,
        "total": total,
        "average": average,
    }

    # 리스트에 차곡차곡 담습니다.
    students.append(student)


# ---------------------------------------------------------------
# 3. 표 형태로 출력합니다
#    f-string 의 자리 맞추기( <  >  ^ )를 활용합니다
# ---------------------------------------------------------------

print("\n")
print("=" * 62)
print(f"{'이름':^8}{'학번':^12}{'전공':^8}{'국어':>6}{'영어':>6}{'수학':>6}{'총점':>7}{'평균':>8}")
print("-" * 62)

for s in students:
    print(
        f"{s['name']:^8}{s['id']:^12}{s['major']:^8}"
        f"{s['kor']:>6}{s['eng']:>6}{s['math']:>6}"
        f"{s['total']:>7}{s['average']:>8.1f}"
    )

print("=" * 62)


# ---------------------------------------------------------------
# 4. 요약 통계
# ---------------------------------------------------------------

# 리스트 안에서 원하는 값만 뽑아 새 리스트를 만듭니다.
averages = []
for s in students:
    averages.append(s["average"])

class_average = sum(averages) / len(averages)

# max() 에 key 를 주면 '무엇을 기준으로 가장 큰지' 정할 수 있습니다.
top_student = max(students, key=lambda s: s["average"])
low_student = min(students, key=lambda s: s["average"])

print(f"\n반 평균   : {class_average:.2f}점")
print(f"최고 성적 : {top_student['name']} ({top_student['average']:.1f}점)")
print(f"최저 성적 : {low_student['name']} ({low_student['average']:.1f}점)")


# ---------------------------------------------------------------
# 5. 등수 매기기
# ---------------------------------------------------------------

ranked = sorted(students, key=lambda s: s["average"], reverse=True)

print("\n[ 석차 ]")
for rank, s in enumerate(ranked, start=1):
    # 평균 90 이상이면 별 표시를 붙여 봅니다.
    mark = " ★" if s["average"] >= 90 else ""
    print(f"{rank}등  {s['name']:<8} {s['average']:.1f}점{mark}")


# ===============================================================
# 더 해보기
# ===============================================================
# 1) 평균이 60점 미만인 학생에게 "(재시험)" 을 붙여 출력해 보세요.
# 2) 과목별 평균(국어 평균, 영어 평균, 수학 평균)도 출력해 보세요.
# 3) 학점을 매겨 보세요. 90이상 A, 80이상 B, 70이상 C, 나머지 F
#    (조건문은 2일차에 배웁니다. 미리 도전해 보세요!)
