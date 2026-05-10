import os
from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic

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
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = build_user_prompt(payload)

    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=220,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        async for text in stream.text_stream:
            if text:
                yield f"data: {text}\n\n"

    yield "data: [DONE]\n\n"
