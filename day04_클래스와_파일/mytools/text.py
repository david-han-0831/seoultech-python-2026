"""문자열 출력과 관련된 함수들을 모아 둔 모듈."""


def make_line(char="=", width=50):
    """구분선 문자열을 만듭니다."""
    return char * width


def make_title(text, char="=", width=50):
    """제목 블록을 만듭니다."""
    line = make_line(char, width)
    return f"{line}\n {text}\n{line}"


def mask_name(name):
    """이름의 가운데를 O 로 가립니다.

    '한동윤' → '한O윤'  /  '김철수' → '김O수'  /  '이영' → '이O'
    """
    if len(name) <= 1:
        return name
    if len(name) == 2:
        return name[0] + "O"
    return name[0] + "O" * (len(name) - 2) + name[-1]


def format_won(amount):
    """숫자를 '1,234원' 형태로 바꿉니다."""
    return f"{amount:,}원"


def truncate(text, limit=20, suffix="..."):
    """긴 문자열을 잘라 냅니다."""
    if len(text) <= limit:
        return text
    return text[:limit] + suffix


def progress_bar(current, total, width=20):
    """텍스트 진행바를 만듭니다.  [████------] 40%"""
    if total <= 0:
        return "[" + "-" * width + "] 0%"
    ratio = min(current / total, 1.0)
    filled = int(width * ratio)
    return "[" + "█" * filled + "-" * (width - filled) + f"] {ratio * 100:.0f}%"


if __name__ == "__main__":
    print("[text.py 자체 테스트]")
    print(make_title("테스트"))
    print(mask_name("한동윤"), mask_name("김철수"), mask_name("이영"))
    print(format_won(1234567))
    print(truncate("아주 긴 문자열입니다. 잘려야 합니다.", 10))
    for i in [0, 5, 10]:
        print(progress_bar(i, 10))
