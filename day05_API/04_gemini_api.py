"""
5일차 - 04. Google Gemini API 연동

생성형 AI 에게 프로그램으로 질문을 보내고 답을 받아 옵니다.
별도 SDK 없이 requests 만으로 호출합니다. (REST API)

[사전 준비]
 1) https://aistudio.google.com/apikey 접속 (구글 로그인)
 2) 'Create API key' 클릭
 3) 프로젝트 루트의 .env 에 붙여넣기
      GEMINI_API_KEY=여기에붙여넣기

키가 없으면 실행 방법만 안내하고 종료합니다.
"""

import os
import textwrap

import requests
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join("..", ".env"))

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


# ---------------------------------------------------------------
# 1. 기본 호출 함수
# ---------------------------------------------------------------

def ask_gemini(prompt, temperature=0.7, max_tokens=1024):
    """Gemini 에게 질문을 보내고 답변 문자열을 돌려줍니다.

    Args:
        prompt: 질문 내용
        temperature: 0에 가까울수록 일관된 답, 1에 가까울수록 창의적인 답
        max_tokens: 답변 최대 길이

    Returns:
        답변 문자열. 실패하면 None.
    """
    if not API_KEY:
        print("[오류] GEMINI_API_KEY 가 설정되지 않았습니다.")
        return None

    # 요청 본문 - Gemini API 가 정한 형식입니다
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,      # 키는 헤더로 보냅니다
    }

    try:
        # 조회가 아니라 '생성 요청'이므로 POST 를 씁니다.
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("[오류] 응답 시간 초과 (30초)")
        return None
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        print(f"[오류] HTTP {code}")
        if code == 400:
            print("  요청 형식이 잘못되었거나 키가 유효하지 않습니다.")
        elif code == 429:
            print("  요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.")
        print(f"  응답: {e.response.text[:300]}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[오류] 요청 실패: {e}")
        return None

    # 응답 구조에서 텍스트만 꺼냅니다.
    #   candidates[0] > content > parts[0] > text
    try:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        print("[오류] 응답 구조가 예상과 다릅니다.")
        print(f"  받은 내용: {response.text[:300]}")
        return None


def print_answer(title, answer, width=70):
    """답변을 보기 좋게 출력합니다."""
    print("\n" + "=" * width)
    print(f" {title}")
    print("=" * width)

    if answer is None:
        print(" (답변을 받지 못했습니다)")
        return

    # 긴 줄을 적당히 접어 줍니다.
    for line in answer.split("\n"):
        if not line.strip():
            print()
            continue
        for wrapped in textwrap.wrap(line, width=width - 2):
            print(f" {wrapped}")


# ---------------------------------------------------------------
# 2. 예제 모음
# ---------------------------------------------------------------

def example_basic():
    """가장 단순한 질문."""
    answer = ask_gemini("파이썬의 리스트와 튜플 차이를 세 줄로 설명해줘.")
    print_answer("예제 1. 기본 질문", answer)


def example_code_review():
    """코드를 주고 검토받기."""
    code = """
def calc(a, b):
    result = a / b
    return result
"""
    prompt = f"""아래 파이썬 코드의 문제점을 찾고 개선된 코드를 알려줘.
설명은 한국어로, 간단히 해줘.

```python
{code}
```"""
    answer = ask_gemini(prompt, temperature=0.3)     # 정확한 답이 필요하니 낮게
    print_answer("예제 2. 코드 리뷰", answer)


def example_data_summary():
    """데이터를 주고 요약시키기 - 03번에서 받은 미세먼지 데이터 활용."""
    data = """
종로구 PM10 45, PM2.5 23
중구 PM10 38, PM2.5 19
강남구 PM10 82, PM2.5 41
송파구 PM10 155, PM2.5 88
"""
    prompt = f"""아래는 오늘 서울의 대기오염 측정값이다.
이 데이터를 바탕으로 시민에게 보낼 안내 문자를 2~3문장으로 작성해줘.
과장하지 말고 사실 위주로 써줘.

{data}"""
    answer = ask_gemini(prompt, temperature=0.5)
    print_answer("예제 3. 데이터 요약 (미세먼지 안내문 생성)", answer)


def example_structured():
    """정해진 형식으로 답변받기 - 프로그램에서 쓰기 좋게."""
    prompt = """'파이썬 입문자가 자주 하는 실수' 3가지를 아래 형식으로만 답해줘.
다른 말은 붙이지 마.

1. 제목 | 설명
2. 제목 | 설명
3. 제목 | 설명"""

    answer = ask_gemini(prompt, temperature=0.2)
    print_answer("예제 4. 형식을 지정한 답변", answer)

    # 답변을 파싱해 프로그램에서 쓸 수 있게 만듭니다.
    if answer:
        print("\n[파싱 결과]")
        for line in answer.strip().split("\n"):
            if "|" not in line:
                continue
            title, desc = line.split("|", 1)
            # "1. 제목" 에서 번호를 떼어냅니다
            title = title.split(".", 1)[-1].strip()
            print(f"  · {title}: {desc.strip()}")


def example_chat():
    """대화 이어가기 - 이전 내용을 함께 보내야 문맥이 유지됩니다."""
    history = []

    questions = [
        "파이썬에서 리스트를 정렬하는 방법을 한 문장으로 알려줘.",
        "방금 말한 방법으로 내림차순 정렬하는 코드를 보여줘.",
    ]

    print("\n" + "=" * 70)
    print(" 예제 5. 문맥을 이어가는 대화")
    print("=" * 70)

    for question in questions:
        history.append(f"사용자: {question}")

        # 지금까지의 대화를 통째로 넘깁니다.
        # (API 는 이전 대화를 기억하지 못합니다)
        prompt = "\n".join(history) + "\nAI:"
        answer = ask_gemini(prompt, temperature=0.4)

        print(f"\n👤 {question}")
        if answer:
            print(f"🤖 {answer.strip()[:400]}")
            history.append(f"AI: {answer}")
        else:
            break


# ---------------------------------------------------------------
# 3. 실행
# ---------------------------------------------------------------

def main():
    if not API_KEY:
        print("=" * 70)
        print(" Gemini API 키가 설정되지 않았습니다")
        print("=" * 70)
        print("""
 [발급 방법]
   1. https://aistudio.google.com/apikey 접속 (구글 로그인)
   2. 'Create API key' 클릭
   3. 생성된 키 복사

 [설정 방법]
   1. 프로젝트 루트에서 .env.example 을 복사해 .env 를 만드세요
        copy .env.example .env
   2. .env 파일을 열어 키를 붙여넣으세요
        GEMINI_API_KEY=AIza...

 [주의]
   .env 파일은 절대 깃허브에 올리지 마세요.
   (.gitignore 에 이미 등록해 두었습니다)
""")
        print("=" * 70)
        return

    print(f"모델: {MODEL}")

    example_basic()
    example_code_review()
    example_data_summary()
    example_structured()
    example_chat()

    print("\n" + "=" * 70)
    print(" 무료 사용량에 한도가 있습니다. 반복 호출에 주의하세요.")
    print("=" * 70)


if __name__ == "__main__":
    main()


# ===============================================================
# 연습 문제
# ===============================================================
# 1) 사용자에게 질문을 입력받아 답변을 출력하는 대화 프로그램을 만드세요.
#    ('종료' 를 입력하면 끝나게 하세요)
#
# 2) 03번에서 받은 실제 미세먼지 데이터를 Gemini 에게 넘겨
#    오늘의 외출 조언을 받아 보세요.
#
# 3) 영어 문장을 입력받아 한국어로 번역하는 함수를 만드세요.
#
# 4) 대화 내용을 JSON 파일에 저장했다가 다음 실행 때 이어가게 하세요.
#    (4일차 JSON 활용)
#
# 5) temperature 를 0.0 과 1.0 으로 바꿔 가며 같은 질문을 던져 보고
#    답변이 어떻게 달라지는지 비교해 보세요.
