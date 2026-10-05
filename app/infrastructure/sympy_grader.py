"""So khớp đáp án bằng sympy (kiểm tra tương đương biểu thức)."""
import re

import sympy
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, standard_transformations)

from app.service.ports import AnswerGrader, GradeVerdict

_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


def _clean(s: str) -> str:
    s = s.strip().strip("$").replace("\\left", "").replace("\\right", "")
    s = s.replace("\\cdot", "*").replace("\\times", "*")
    s = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = s.replace("{", "(").replace("}", ")").replace("\\", "")
    if "=" in s:  # "x = 4" -> lấy vế phải
        s = s.split("=")[-1]
    return s.strip()


def _parse(s: str):
    return parse_expr(_clean(s), transformations=_TRANSFORMS)


class SympyAnswerGrader(AnswerGrader):
    def grade(self, expected: str, actual: str) -> GradeVerdict:
        try:
            ok = sympy.simplify(_parse(expected) - _parse(actual)) == 0
        except Exception:
            ok = _clean(expected).replace(" ", "").lower() == _clean(actual).replace(" ", "").lower()
        msg = "Đáp án đúng." if ok else f"Đáp án chưa đúng. Đáp án đúng: {expected}"
        return GradeVerdict(is_correct=bool(ok), feedback=msg)
