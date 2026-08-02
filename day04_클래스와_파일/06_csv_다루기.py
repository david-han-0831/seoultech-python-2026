"""
4일차 - 06. CSV 파일 다루기

CSV(Comma-Separated Values)는 쉼표로 구분된 표 데이터입니다.
엑셀에서 바로 열리기 때문에 실무에서 데이터를 주고받을 때 가장 많이 씁니다.

    이름,국어,영어,수학
    김철수,90,85,77
    이영희,88,92,95
"""

import csv
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_PATH = os.path.join(OUTPUT_DIR, "scores.csv")


# ---------------------------------------------------------------
# 1. 직접 만들어 보면 - csv 모듈이 왜 필요한지
# ---------------------------------------------------------------

# 그냥 문자열로 처리하면 이렇게 됩니다.
line = "김철수,90,85,77"
parts = line.split(",")
print(parts)     # ['김철수', '90', '85', '77']

# 하지만 값 안에 쉼표가 들어가면 깨집니다.
tricky = '김철수,"서울시 노원구, 공릉동",90'
print(tricky.split(","))     # 주소가 두 조각으로 잘려 버립니다!

# csv 모듈은 이런 경우를 알아서 처리해 줍니다.


# ---------------------------------------------------------------
# 2. csv.writer - 리스트를 CSV 로 저장
# ---------------------------------------------------------------

header = ["이름", "국어", "영어", "수학"]
rows = [
    ["김철수", 90, 85, 77],
    ["이영희", 88, 92, 95],
    ["박민수", 70, 65, 80],
    ["최지우", 100, 98, 96],
]

# newline="" 은 윈도우에서 빈 줄이 하나씩 끼는 문제를 막아 줍니다. 꼭 넣으세요.
with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)      # 한 줄
    writer.writerows(rows)       # 여러 줄

print(f"\n'{CSV_PATH}' 저장 완료")

# [중요] encoding="utf-8-sig" 를 쓰는 이유
#   그냥 utf-8 로 저장하면 엑셀에서 열었을 때 한글이 깨집니다.
#   utf-8-sig 는 파일 앞에 표식(BOM)을 넣어 엑셀이 알아보게 합니다.


# ---------------------------------------------------------------
# 3. csv.reader - CSV 읽기
# ---------------------------------------------------------------

with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)        # 첫 줄(헤더)을 따로 꺼냄

    print(f"\n헤더: {header}")
    for row in reader:
        print(f"  {row}")        # 값은 전부 '문자열'로 읽힙니다


# ---------------------------------------------------------------
# 4. csv.DictReader - 딕셔너리로 읽기 (훨씬 편합니다)
# ---------------------------------------------------------------

with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)   # 첫 줄을 자동으로 키로 씁니다
    students = list(reader)

print("\n[DictReader 로 읽기]")
for s in students:
    print(f"  {s}")

# 값은 문자열이므로 계산하려면 int() 로 바꿔야 합니다.
print("\n[평균 계산]")
for s in students:
    scores = [int(s["국어"]), int(s["영어"]), int(s["수학"])]
    avg = sum(scores) / len(scores)
    print(f"  {s['이름']}: 평균 {avg:.1f}")


# ---------------------------------------------------------------
# 5. csv.DictWriter - 딕셔너리를 CSV 로 저장
# ---------------------------------------------------------------

data = [
    {"이름": "김철수", "전공": "ITM", "평균": 84.0},
    {"이름": "이영희", "전공": "ITM", "평균": 91.7},
    {"이름": "박민수", "전공": "산업공학", "평균": 71.7},
]

result_path = os.path.join(OUTPUT_DIR, "result.csv")

with open(result_path, "w", encoding="utf-8-sig", newline="") as f:
    fieldnames = ["이름", "전공", "평균"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()         # 헤더 자동 작성
    writer.writerows(data)

print(f"\n'{result_path}' 저장 완료")


# ---------------------------------------------------------------
# 6. 실전 - CSV 를 읽어 가공하고 다시 저장하기
# ---------------------------------------------------------------

def load_scores(filepath):
    """성적 CSV 를 읽어 계산까지 마친 리스트로 돌려줍니다."""
    result = []

    try:
        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                try:
                    scores = [int(row["국어"]), int(row["영어"]), int(row["수학"])]
                except ValueError:
                    # 숫자가 아닌 값이 섞여 있으면 그 줄은 건너뜁니다.
                    print(f"  [경고] '{row.get('이름')}' 행의 점수를 읽을 수 없습니다.")
                    continue

                total = sum(scores)
                average = total / len(scores)

                result.append({
                    "이름": row["이름"],
                    "국어": scores[0],
                    "영어": scores[1],
                    "수학": scores[2],
                    "총점": total,
                    "평균": round(average, 1),
                    "학점": to_grade(average),
                })
    except FileNotFoundError:
        print(f"  [오류] '{filepath}' 파일이 없습니다.")

    return result


def to_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def save_report(data, filepath):
    """계산 결과를 CSV 로 저장합니다."""
    if not data:
        print("  저장할 데이터가 없습니다.")
        return

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"  '{filepath}' 저장 완료 ({len(data)}건)")


print("\n[성적 처리]")
records = load_scores(CSV_PATH)

# 평균 높은 순으로 정렬
records.sort(key=lambda r: r["평균"], reverse=True)

print(f"\n{'순위':^5}{'이름':^8}{'총점':>6}{'평균':>8}{'학점':>6}")
print("-" * 34)
for rank, r in enumerate(records, start=1):
    print(f"{rank:^5}{r['이름']:^8}{r['총점']:>6}{r['평균']:>8}{r['학점']:>6}")
print("-" * 34)

report_path = os.path.join(OUTPUT_DIR, "report.csv")
save_report(records, report_path)


# ---------------------------------------------------------------
# 7. 구분자가 쉼표가 아닌 경우
# ---------------------------------------------------------------

tsv_path = os.path.join(OUTPUT_DIR, "data.tsv")

# 탭으로 구분된 파일(TSV)
with open(tsv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["이름", "점수"])
    writer.writerow(["김철수", 90])

with open(tsv_path, "r", encoding="utf-8", newline="") as f:
    for row in csv.reader(f, delimiter="\t"):
        print(row)


# ---------------------------------------------------------------
# 8. 자주 겪는 문제 정리
# ---------------------------------------------------------------
#
#  Q. 엑셀에서 열면 한글이 깨져요
#     → encoding="utf-8-sig" 로 저장하세요.
#
#  Q. 저장했더니 줄 사이에 빈 줄이 생겨요 (윈도우)
#     → open() 에 newline="" 을 넣으세요.
#
#  Q. 숫자를 더하려는데 문자열이 이어붙습니다
#     → CSV 에서 읽은 값은 전부 문자열입니다. int()/float() 로 바꾸세요.
#
#  Q. 파일이 열려 있어서 저장이 안 됩니다 (PermissionError)
#     → 엑셀에서 그 파일을 닫고 다시 실행하세요.
#
#  * 2주차에 배울 pandas 를 쓰면 이 모든 게 두세 줄로 끝납니다.
#    pd.read_csv() / df.to_csv()


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 학생 정보를 입력받아 CSV 에 계속 추가하는 프로그램을 만드세요.
#
# 2) CSV 를 읽어 평균 80점 이상인 학생만 별도 파일로 저장하세요.
#
# 3) 두 개의 CSV(학생 정보 / 성적)를 읽어 이름 기준으로 합치세요.
#
# 4) CSV 의 특정 열을 기준으로 정렬해 새 파일로 저장하는
#    함수를 만드세요. (정렬 기준을 인자로 받도록)
