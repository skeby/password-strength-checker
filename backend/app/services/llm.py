import os
from collections.abc import AsyncIterator

from groq import AsyncGroq

from app.models.schemas import AdviseRequest


SYSTEM_PROMPT = """You are a concise password security advisor. You will be given a structured
analysis of a password. Your job is to explain in plain English — in 2 to 3
sentences — why the password is strong or weak, and give exactly one specific,
actionable suggestion. Do not repeat raw numbers. Do not use jargon. Do not
be alarmist. End with the suggestion on a new line prefixed with "Suggestion:"."""


def _detected_patterns(payload: AdviseRequest) -> str:
    flags: list[str] = []
    if payload.hasDictionaryMatch:
        flags.append("dictionary match")
    if payload.hasL33tSub:
        flags.append("l33t substitutions")
    if payload.hasKeyboardPattern:
        flags.append("keyboard pattern")
    if payload.hasDatePattern:
        flags.append("date pattern")
    if payload.hasRepeat:
        flags.append("repeated characters")
    if payload.hasSequence:
        flags.append("sequence pattern")
    return ", ".join(flags) if flags else "none"


def build_user_prompt(payload: AdviseRequest) -> str:
    breached_text = (
        f"true ({payload.breachCount} times)"
        if payload.isBreached
        else "false"
    )
    return f"""Password analysis:
- Strength score: {payload.strengthScore}/100 (from ML model)
- zxcvbn score: {payload.zxcvbnScore}/4
- Estimated crack time: {payload.crackTime}
- zxcvbn warning: "{payload.warning}"
- Patterns detected: {_detected_patterns(payload)}
- Policy rules passed: {payload.rulesPassed}/{payload.rulesTotal}
- Found in known breaches: {breached_text}
Give your explanation now."""


async def stream_advice(payload: AdviseRequest) -> AsyncIterator[str]:
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = build_user_prompt(payload)

    stream = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=220,
        stream=True,
    )

    async for chunk in stream:
        text = chunk.choices[0].delta.content if chunk.choices else None
        if text:
            yield f"data: {text}\n\n"

    yield "data: [DONE]\n\n"
