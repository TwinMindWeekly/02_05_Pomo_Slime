import json
import os
import time
from brain.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class SlimeResponse:
    """Kết quả phản hồi từ AI đã được parse và validate."""

    VALID_STATUSES = ("Happy", "Sad", "Angry", "Evolving")

    def __init__(self, status: str, message: str, energy_change: int):
        self.status = status
        self.message = message
        self.energy_change = energy_change

    @classmethod
    def default(cls) -> "SlimeResponse":
        """Phản hồi mặc định khi AI không khả dụng hoặc lỗi."""
        return cls(status="Sad", message="Bé đang buồn ngủ xíu, chờ xíu nha...", energy_change=0)

    def __repr__(self):
        return f"SlimeResponse(status={self.status}, energy={self.energy_change:+d}, msg={self.message!r})"


class BrainHandler:
    """
    Kết nối Groq hoặc Gemini để tạo phản hồi cho bé PomoSlime.
    - Ưu tiên Groq (tốc độ cao, free tier).
    - Fallback sang Gemini Flash nếu Groq lỗi.
    - Rate limiting 30s để không spam API.
    """

    MIN_CALL_INTERVAL = 30  # giây

    def __init__(self, groq_api_key: str = None, gemini_api_key: str = None):
        self._last_call_time: float = 0.0
        self._groq_client = None
        self._gemini_model = None

        # ---- Groq setup ----
        groq_key = groq_api_key or os.getenv("GROQ_API_KEY", "")
        if groq_key:
            try:
                from groq import Groq
                self._groq_client = Groq(api_key=groq_key)
                print("[Brain] ✓ Groq sẵn sàng (llama-3.1-8b-instant)")
            except ImportError:
                print("[Brain] ✗ Groq chưa cài — chạy: pip install groq")
            except Exception as e:
                print(f"[Brain] ✗ Groq lỗi: {e}")

        # ---- Gemini setup (fallback) ----
        gemini_key = gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                self._gemini_model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash",
                    system_instruction=SYSTEM_PROMPT
                )
                print("[Brain] ✓ Gemini sẵn sàng (gemini-2.0-flash)")
            except ImportError:
                print("[Brain] ✗ google-generativeai chưa cài — chạy: pip install google-generativeai")
            except Exception as e:
                print(f"[Brain] ✗ Gemini lỗi: {e}")

        if not self._groq_client and not self._gemini_model:
            print("[Brain] ⚠ Không có API key nào. Chạy ở chế độ offline (SlimeResponse.default).")

    # ---- Public API ----

    def analyze(self, process_name: str, app_type: str,
                window_title: str, minutes_used: float = 0.0, is_pomodoro: bool = False) -> SlimeResponse:
        """
        Phân tích ngữ cảnh và trả về phản hồi SlimeResponse.
        Có rate limiting để bảo vệ free tier quota.
        """
        now = time.time()
        elapsed = now - self._last_call_time
        
        # Bỏ qua rate limit đối với các sự kiện hệ thống
        if app_type not in ["Startup", "Report"]:
            if elapsed < self.MIN_CALL_INTERVAL:
                print(f"[Brain] Rate limit — còn {self.MIN_CALL_INTERVAL - elapsed:.0f}s")
                return None

        self._last_call_time = now
        user_msg = USER_PROMPT_TEMPLATE.format(
            process_name=process_name,
            app_type=app_type,
            window_title=window_title[:100],
            is_pomodoro=is_pomodoro,
            minutes_used=round(minutes_used, 1)
        )

        # Thử Groq → fallback Gemini
        if self._groq_client:
            resp = self._call_groq(user_msg)
            if resp:
                return resp

        if self._gemini_model:
            resp = self._call_gemini(user_msg)
            if resp:
                return resp

        return SlimeResponse.default()

    # ---- Internal ----

    def _call_groq(self, user_message: str) -> "SlimeResponse | None":
        """Gọi Groq API với llama-3.1-8b-instant (free tier)."""
        try:
            completion = self._groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,
                max_tokens=150,
                response_format={"type": "json_object"}
            )
            raw = completion.choices[0].message.content
            return self._parse_response(raw)
        except Exception as e:
            print(f"[Brain] Groq lỗi: {e}")
            return None

    def _call_gemini(self, user_message: str) -> "SlimeResponse | None":
        """Gọi Gemini API với gemini-2.0-flash (free tier)."""
        try:
            result = self._gemini_model.generate_content(user_message)
            raw = result.text
            return self._parse_response(raw)
        except Exception as e:
            print(f"[Brain] Gemini lỗi: {e}")
            return None

    def _parse_response(self, raw: str) -> "SlimeResponse | None":
        """Parse và validate JSON response từ AI."""
        try:
            # Làm sạch markdown code blocks
            raw = raw.strip()
            if "```" in raw:
                parts = raw.split("```")
                raw = parts[1] if len(parts) > 1 else raw
                if raw.startswith("json"):
                    raw = raw[4:]

            data = json.loads(raw.strip())
            status = data.get("status", "Sad")
            message = data.get("message", "...")
            energy_change = int(data.get("energy_change", 0))

            # Validate status
            if status not in SlimeResponse.VALID_STATUSES:
                status = "Sad"

            # Clamp energy_change
            energy_change = max(-10, min(10, energy_change))

            return SlimeResponse(status=status, message=message, energy_change=energy_change)

        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            print(f"[Brain] Parse lỗi: {e} | Raw: {raw[:80]!r}")
            return None
