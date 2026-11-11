
from pathlib import Path
from groq import Groq

MODEL = "openai/gpt-oss-20b"

SYSTEM = (Path(__file__).parent / "system_prompt.txt").read_text(
    encoding="utf-8"
)

MAX_MESSAGES = 12


def trimmed(messages: list[dict]) -> list[dict]:
    recent = messages[-MAX_MESSAGES:]

    if recent and recent[0]["role"] == "assistant":
        recent = recent[1:]

    return recent


def get_reply(
    api_key: str,
    messages: list[dict],
    trip_notes: str = "",
    weather: dict | None = None,
) -> str:

    extra = (
        "\nIMPORTANT TRIP FACTS PROVIDED BY THE USER:\n" + trip_notes
        if trip_notes.strip()
        else ""
    )

    if weather:
        extra += (
            "\nVERIFIED WEATHER TOOL RESULT "
            "(Open Meteo, current and short term only):\n"
            + str(weather)
            + "\nDo not extrapolate this forecast to other dates."
        )

    prompt = [
        {"role": "system", "content": SYSTEM + extra}
    ] + trimmed(messages)

    response = Groq(api_key=api_key).chat.completions.create(
        model=MODEL,
        messages=prompt,
        temperature=0.5,
        max_completion_tokens=5000,
        reasoning_effort="low",
        include_reasoning=False,
    )

    
    choice = response.choices[0]

    print("Finish reason:", choice.finish_reason)
    print("Completion tokens:", response.usage.completion_tokens)
    print("Prompt tokens:", response.usage.prompt_tokens)

    answer = (choice.message.content or "").strip()


    if choice.finish_reason == "length":
        answer += (
            "\n\n*This answer reached its length limit. "
            "Ask me to continue.*"
        )

    return answer
