"""
4일차 - 05. 파일 입출력 (File I/O)

지금까지 만든 프로그램은 껐다 켜면 데이터가 사라졌습니다.
파일에 저장하면 다음에 다시 불러올 수 있습니다.
"""

import os

# 결과 파일을 모아 둘 폴더를 만듭니다. (이미 있으면 그냥 넘어갑니다)
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------
# 1. 파일 쓰기 - with 문을 쓰세요
# ---------------------------------------------------------------

path = os.path.join(OUTPUT_DIR, "hello.txt")

# with 를 쓰면 블록이 끝날 때 파일이 자동으로 닫힙니다.
with open(path, "w", encoding="utf-8") as f:
    f.write("첫 번째 줄입니다.\n")      # 줄바꿈은 직접 \n 을 넣어야 합니다
    f.write("두 번째 줄입니다.\n")

print(f"'{path}' 에 저장했습니다.")

# [중요] 한글이 깨지지 않으려면 encoding="utf-8" 을 꼭 붙이세요.
#        윈도우 기본 인코딩(cp949) 때문에 자주 문제가 생깁니다.

# with 없이 쓰면 close() 를 직접 해야 합니다. (권장하지 않습니다)
#   f = open(path, "w")
#   f.write("...")
#   f.close()      ← 잊어버리면 파일이 잠기거나 내용이 안 써질 수 있습니다


# ---------------------------------------------------------------
# 2. 파일 모드
# ---------------------------------------------------------------
#
#   "w"  쓰기   - 파일이 있으면 내용을 전부 지우고 새로 씀 (주의!)
#   "a"  추가   - 기존 내용 뒤에 이어 씀
#   "r"  읽기   - 읽기 전용 (기본값). 파일이 없으면 에러
#   "x"  생성   - 파일이 이미 있으면 에러
#   "rb" "wb"   - 이미지 등 바이너리 파일용

# 추가 모드
with open(path, "a", encoding="utf-8") as f:
    f.write("나중에 덧붙인 줄입니다.\n")


# ---------------------------------------------------------------
# 3. 파일 읽기 - 세 가지 방법
# ---------------------------------------------------------------

# 3-1. read() : 파일 전체를 문자열 하나로
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
print("\n[read()]")
print(content)

# 3-2. readlines() : 줄 단위 리스트로
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print("[readlines()]")
print(lines)     # 각 줄 끝에 \n 이 붙어 있습니다

# \n 을 없애려면
with open(path, "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]
print(lines)

# 3-3. for 문으로 한 줄씩 (파일이 클 때 메모리를 아낍니다) ← 권장
print("\n[한 줄씩]")
with open(path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"  {i}: {line.strip()}")


# ---------------------------------------------------------------
# 4. 파일이 없을 때 대비하기
# ---------------------------------------------------------------

def read_file(filepath):
    """파일을 읽습니다. 없으면 빈 문자열을 돌려줍니다."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[알림] '{filepath}' 파일이 없습니다.")
        return ""
    except UnicodeDecodeError:
        print(f"[알림] '{filepath}' 인코딩을 읽을 수 없습니다.")
        return ""


print()
print(repr(read_file("없는파일.txt")))

# 파일 존재 여부를 미리 확인할 수도 있습니다.
if os.path.exists(path):
    print(f"'{path}' 크기: {os.path.getsize(path)} 바이트")


# ---------------------------------------------------------------
# 5. 리스트를 파일로 저장하고 다시 불러오기
# ---------------------------------------------------------------

todo_path = os.path.join(OUTPUT_DIR, "todo.txt")

todos = ["파이썬 복습하기", "과제 제출하기", "운동하기"]

# 저장
with open(todo_path, "w", encoding="utf-8") as f:
    for todo in todos:
        f.write(todo + "\n")

# writelines 를 쓰면 반복문 없이도 됩니다. (줄바꿈은 직접 넣어야 함)
with open(todo_path, "w", encoding="utf-8") as f:
    f.writelines(todo + "\n" for todo in todos)

# 불러오기
with open(todo_path, "r", encoding="utf-8") as f:
    loaded = [line.strip() for line in f if line.strip()]   # 빈 줄 제외

print(f"\n불러온 할 일: {loaded}")
print(f"원본과 같은가: {todos == loaded}")


# ---------------------------------------------------------------
# 6. 실전 - 간단한 메모장
# ---------------------------------------------------------------

from datetime import datetime

memo_path = os.path.join(OUTPUT_DIR, "memo.txt")


def write_memo(text):
    """메모를 시간과 함께 덧붙입니다."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(memo_path, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text}\n")


def read_memos():
    """저장된 메모를 모두 읽습니다."""
    if not os.path.exists(memo_path):
        return []
    with open(memo_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


write_memo("첫 번째 메모입니다.")
write_memo("파이썬 특강 1주차 진행 중")

print("\n[메모 목록]")
for i, memo in enumerate(read_memos(), start=1):
    print(f"  {i}. {memo}")


# ---------------------------------------------------------------
# 7. 실전 - 텍스트 파일 분석
# ---------------------------------------------------------------

sample_path = os.path.join(OUTPUT_DIR, "sample.txt")

sample_text = """파이썬은 배우기 쉬운 프로그래밍 언어입니다.
파이썬은 데이터 분석에 강합니다.
파이썬으로 웹 개발도 할 수 있습니다.
많은 회사가 파이썬을 사용합니다."""

with open(sample_path, "w", encoding="utf-8") as f:
    f.write(sample_text)

# 분석
with open(sample_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

total_chars = sum(len(line) for line in lines)
all_words = []
for line in lines:
    all_words.extend(line.split())

print("\n[파일 분석]")
print(f"  줄 수    : {len(lines)}")
print(f"  글자 수  : {total_chars}")
print(f"  단어 수  : {len(all_words)}")

from collections import Counter
word_count = Counter(all_words)
print("  자주 나온 단어:")
for word, count in word_count.most_common(3):
    print(f"    {word}: {count}회")

# 특정 단어가 들어간 줄 찾기
keyword = "파이썬"
print(f"\n  '{keyword}' 가 들어간 줄:")
for i, line in enumerate(lines, start=1):
    if keyword in line:
        print(f"    {i}번째 줄: {line}")


# ---------------------------------------------------------------
# 8. 파일과 폴더 다루기 (os 모듈)
# ---------------------------------------------------------------

print(f"\n현재 작업 폴더: {os.getcwd()}")
print(f"output 폴더의 파일 목록: {os.listdir(OUTPUT_DIR)}")

# 경로 합치기 - 운영체제마다 구분자가 달라서 직접 이어붙이면 안 됩니다.
print(os.path.join("폴더", "하위폴더", "파일.txt"))

# 파일명과 확장자 분리
filename = "report_2026.xlsx"
name, ext = os.path.splitext(filename)
print(f"이름: {name}, 확장자: {ext}")

# 파일 삭제 (조심해서 쓰세요)
# os.remove(path)


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 사용자에게 여러 줄을 입력받아(빈 줄 입력 시 종료) 파일에 저장하세요.
#
# 2) 저장한 파일을 읽어 줄 번호를 붙여 출력하세요.
#
# 3) 2일차 '숫자 맞추기 게임'의 최고 기록을 파일에 저장하고
#    다음 실행 때 불러오도록 만드세요.
#
# 4) 텍스트 파일에서 특정 단어를 다른 단어로 모두 바꿔
#    새 파일로 저장하는 프로그램을 만드세요.
