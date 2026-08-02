"""
4일차 - 08. 모듈과 패키지

모듈  : .py 파일 하나
패키지: .py 파일들을 모아 둔 폴더 (__init__.py 가 들어 있음)

코드가 길어지면 파일을 나누고, import 로 가져다 씁니다.

이 폴더 구조를 보세요.
    day04_클래스와_파일/
      ├─ 08_모듈과_패키지.py   ← 지금 이 파일
      └─ mytools/              ← 패키지
           ├─ __init__.py
           ├─ score.py         ← 모듈
           └─ text.py          ← 모듈
"""

# ---------------------------------------------------------------
# 1. 표준 라이브러리 import - 설치 없이 바로 쓰는 것들
# ---------------------------------------------------------------

import math
import random
import os
from datetime import datetime, timedelta

print(math.pi)              # 3.141592653589793
print(math.sqrt(16))        # 4.0
print(math.ceil(3.2))       # 4  올림
print(math.floor(3.8))      # 3  내림

print(random.randint(1, 6))              # 1~6 사이 정수
print(random.choice(["가위", "바위", "보"]))
print(random.sample(range(1, 46), 6))    # 로또 번호 (중복 없이 6개)

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
print((now + timedelta(days=7)).strftime("%Y-%m-%d"))   # 일주일 뒤


# ---------------------------------------------------------------
# 2. import 하는 네 가지 방법
# ---------------------------------------------------------------

# 2-1. 모듈 통째로
import math
print(math.sqrt(25))

# 2-2. 필요한 것만 꺼내기 (모듈 이름 없이 바로 씁니다)
from math import sqrt, pi
print(sqrt(25), pi)

# 2-3. 별명 붙이기 (2주차에 pandas 를 pd 로 부르게 됩니다)
import math as m
print(m.sqrt(25))

from datetime import datetime as dt
print(dt.now().year)

# 2-4. 전부 가져오기 - 되도록 쓰지 마세요
# from math import *
#   → 이름이 겹치면 기존 함수를 덮어써 버려서 원인을 찾기 어렵습니다.


# ---------------------------------------------------------------
# 3. 내가 만든 패키지 가져다 쓰기
# ---------------------------------------------------------------

# 방법 A: 패키지에서 바로 (mytools/__init__.py 에 정의해 뒀습니다)
from mytools import to_grade, get_average, is_passed
from mytools import make_line, mask_name, format_won

# 방법 B: 모듈 경로를 다 쓰기
from mytools.score import rank_of
from mytools.text import make_title, progress_bar, truncate

# 방법 C: 모듈 자체를 가져오기
import mytools.score as score

print("\n" + make_title("내가 만든 패키지 사용하기"))

scores = [90, 85, 77]
avg = get_average(scores)

print(f"평균  : {avg:.1f}")
print(f"학점  : {to_grade(avg)}")
print(f"합격  : {is_passed(scores)}")
print(f"석차  : {rank_of(85, [90, 85, 77, 95])}등")
print(f"이름  : {mask_name('한동윤')}")
print(f"금액  : {format_won(1234567)}")
print(f"진행  : {progress_bar(7, 10)}")
print(f"모듈 상수: {score.PASS_CUTOFF}점 이상 합격")


# ---------------------------------------------------------------
# 4. __name__ 과 __main__ - 자주 보게 될 관용구
# ---------------------------------------------------------------

# 파이썬은 파일마다 __name__ 이라는 변수를 자동으로 만듭니다.
#   - 직접 실행한 파일  →  __name__ 은 "__main__"
#   - import 된 파일    →  __name__ 은 모듈 이름 ("mytools.score")

print(f"\n지금 이 파일의 __name__ : {__name__}")
print(f"import 된 score 모듈의 __name__ : {score.__name__}")

# 그래서 아래처럼 쓰면
#   "이 파일을 직접 실행할 때만 돌려라" 라는 뜻이 됩니다.
#
#   if __name__ == "__main__":
#       main()
#
# mytools/score.py 를 직접 실행해 보세요. 테스트 코드가 돌아갑니다.
#   python mytools/score.py
#
# 하지만 import 할 때는 그 부분이 실행되지 않습니다.


# ---------------------------------------------------------------
# 5. 모듈이 어디서 찾아지는지
# ---------------------------------------------------------------

import sys

print("\n[파이썬이 모듈을 찾는 경로]")
for p in sys.path[:4]:
    print(f"  {p if p else '(현재 폴더)'}")

# ModuleNotFoundError 가 나면 대개 두 가지 이유입니다.
#   1) 실행 위치가 달라서 → 이 파일이 있는 폴더에서 실행하세요
#         cd day04_클래스와_파일
#         python 08_모듈과_패키지.py
#   2) 설치가 안 돼서   → pip install 모듈이름


# ---------------------------------------------------------------
# 6. 외부 라이브러리와 pip
# ---------------------------------------------------------------
#
#  표준 라이브러리 : 파이썬에 처음부터 들어 있음 (math, random, json, csv, os)
#  외부 라이브러리 : 따로 설치해야 함 (requests, pandas, matplotlib)
#
#  설치        pip install requests
#  버전 지정   pip install requests==2.32.3
#  목록 보기   pip list
#  목록 저장   pip freeze > requirements.txt
#  한 번에 설치 pip install -r requirements.txt
#
#  5일차부터는 requests, beautifulsoup4 를 씁니다.
#  프로젝트 루트에서 아래를 실행해 두세요.
#      pip install -r requirements.txt


# ---------------------------------------------------------------
# 7. 가상환경 (venv) - 왜 필요한가
# ---------------------------------------------------------------
#
#  프로젝트 A 는 pandas 1.5 가 필요하고
#  프로젝트 B 는 pandas 2.2 가 필요하다면?
#  → 컴퓨터 전체에 하나만 깔면 충돌합니다.
#
#  가상환경은 '프로젝트마다 독립된 설치 공간'을 만들어 줍니다.
#
#      python -m venv venv          가상환경 만들기
#      venv\Scripts\activate        활성화 (윈도우)
#      source venv/bin/activate     활성화 (macOS/Linux)
#      deactivate                   빠져나오기
#
#  활성화되면 터미널 앞에 (venv) 가 붙습니다.


# ---------------------------------------------------------------
# 8. 실전 - 파일을 나눠 정리하는 기준
# ---------------------------------------------------------------
#
#  한 파일이 200~300줄을 넘어가면 나눌 때가 된 것입니다.
#  나누는 기준은 '역할' 입니다.
#
#      project/
#        ├─ main.py           프로그램 시작점
#        ├─ models.py         클래스 정의
#        ├─ storage.py        파일 저장/불러오기
#        ├─ views.py          화면 출력
#        └─ utils.py          잡다한 도우미 함수
#
#  오늘 실습(실습_성적관리_클래스버전.py)은 아직 한 파일이지만,
#  기능이 더 늘어나면 이렇게 나누게 됩니다.


# ===============================================================
# 연습 문제
# ===============================================================
# 1) mytools 에 date.py 모듈을 추가하세요.
#    오늘 날짜 문자열, D-day 계산 함수를 넣으세요.
#
# 2) mytools/score.py 에 '상대평가 등급' 함수를 추가하세요.
#    상위 10% A, 30% B, 70% C, 나머지 D
#
# 3) 지금까지 만든 프로그램에서 반복해 쓴 함수를 찾아
#    mytools 에 모으고 import 해서 쓰도록 바꿔 보세요.
#
# 4) mytools/text.py 를 직접 실행해 테스트 코드가 도는지 확인하고,
#    이 파일에서 import 했을 때는 안 도는지 확인하세요.
