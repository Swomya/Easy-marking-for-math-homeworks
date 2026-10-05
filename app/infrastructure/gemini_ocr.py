"""Adapter OCR dùng Gemini API (SDK google-genai)."""
import json

from google import genai
from google.genai import types

from app.service.errors import OcrError
from app.service.ports import OcrEngine, OcrResult

PROMPT = (
    "Đây là ảnh bài làm toán viết tay của học sinh. "
    "Hãy chép lại chính xác toàn bộ lời giải (dùng LaTeX cho công thức) "
    "và xác định ĐÁP ÁN CUỐI CÙNG học sinh đã viết (không tự giải lại, không sửa lỗi). "
    'Chỉ trả về JSON: {"transcription": "...", "final_answer": "..."}'
)


class GeminiOcrEngine(OcrEngine):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        if not api_key:
            raise ValueError("Thiếu GEMINI_API_KEY")
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def extract(self, image: bytes, mime_type: str) -> OcrResult:
        try:
            resp = self._client.models.generate_content(
                model=self._model,
                contents=[types.Part.from_bytes(data=image, mime_type=mime_type), PROMPT],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", temperature=0.0),
            )
            data = json.loads(resp.text)
            return OcrResult(text=str(data["transcription"]), final_answer=str(data["final_answer"]))
        except Exception as e:  # lỗi mạng, quota, JSON sai...
            raise OcrError(str(e)) from e
