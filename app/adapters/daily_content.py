import httpx
import html
from typing import Optional
from app.schemas.dashboard import DailyQuote, TriviaQuestion, WordOfTheDay, DailyContentModule

class DailyContentAdapter:
    ZEN_QUOTES_URL = "https://zenquotes.io/api/today"
    TRIVIA_URL = "https://opentdb.com/api.php?amount=1&type=multiple"
    FREE_DICT_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    # Daily rotating word targets for live dictionary definition lookup
    ROTATING_WORDS = ["resilient", "ubiquitous", "autonomous", "paradigm", "velocity", "synergy", "pragmatic"]

    @classmethod
    async def fetch_daily_quote(cls) -> Optional[DailyQuote]:
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                res = await client.get(cls.ZEN_QUOTES_URL)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        item = data[0]
                        return DailyQuote(
                            quote=item.get("q", ""),
                            author=item.get("a", "Unknown")
                        )
            except Exception:
                return None
        return None

    @classmethod
    async def fetch_trivia(cls) -> Optional[TriviaQuestion]:
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                res = await client.get(cls.TRIVIA_URL)
                if res.status_code == 200:
                    results = res.json().get("results", [])
                    if results:
                        item = results[0]
                        question = html.unescape(item.get("question", ""))
                        correct = html.unescape(item.get("correct_answer", ""))
                        incorrects = [html.unescape(i) for i in item.get("incorrect_answers", [])]
                        options = incorrects + [correct]
                        options.sort()

                        return TriviaQuestion(
                            question=question,
                            correct_answer=correct,
                            options=options,
                            category=html.unescape(item.get("category", "General")),
                            difficulty=item.get("difficulty", "medium").capitalize()
                        )
            except Exception:
                return None
        return None

    @classmethod
    async def fetch_word_of_the_day(cls) -> Optional[WordOfTheDay]:
        import time
        target_word = cls.ROTATING_WORDS[int(time.time() // 86400) % len(cls.ROTATING_WORDS)]
        url = f"{cls.FREE_DICT_URL}{target_word}"
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        entry = data[0]
                        meanings = entry.get("meanings", [])
                        if meanings:
                            meaning = meanings[0]
                            pos = meaning.get("partOfSpeech", "noun")
                            defs = meaning.get("definitions", [])
                            if defs:
                                definition = defs[0].get("definition", "")
                                example = defs[0].get("example", f"The word '{target_word}' is commonly used in English.")
                                return WordOfTheDay(
                                    word=target_word.capitalize(),
                                    definition=definition,
                                    part_of_speech=pos,
                                    example=example
                                )
            except Exception:
                return None
        return None

    @classmethod
    async def get_daily_content_module(cls) -> DailyContentModule:
        quote = await cls.fetch_daily_quote()
        trivia = await cls.fetch_trivia()
        word = await cls.fetch_word_of_the_day()
        return DailyContentModule(
            quote=quote,
            trivia=trivia,
            word_of_the_day=word
        )
