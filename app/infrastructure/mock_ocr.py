"""OCR giả: trả kết quả tức thì, dùng cho test & kiểm thử tải."""
from app.service.ports import OcrEngine, OcrResult


class MockOcrEngine(OcrEngine):
    def __init__(self, answer: str = "4"):
        self._answer = answer

    def extract(self, image: bytes, mime_type: str) -> OcrResult:
        return OcrResult(text=f"2x = 8 => x = {self._answer}", final_answer=f"x = {self._answer}")
