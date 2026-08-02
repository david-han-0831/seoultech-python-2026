"""
mytools 패키지

폴더 안에 __init__.py 가 있으면 그 폴더는 '패키지'가 됩니다.
이 파일은 비어 있어도 되지만, 자주 쓰는 것을 미리 꺼내 두면 편합니다.

    from mytools import to_grade        ← 이렇게 짧게 쓸 수 있게 됩니다
    (원래는 from mytools.score import to_grade)
"""

from .score import to_grade, get_average, is_passed
from .text import make_line, mask_name, format_won

# from 패키지 import * 했을 때 딸려 나올 이름들
__all__ = [
    "to_grade",
    "get_average",
    "is_passed",
    "make_line",
    "mask_name",
    "format_won",
]

__version__ = "1.0"
