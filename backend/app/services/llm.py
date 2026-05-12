import os
from collections.abc import AsyncIterator

from groq import AsyncGroq

from app.models.schemas import AdviseRequest


SYSTEM_PROMPT = """You are a password security advisor. You will receive a structured analysis
of a password including expert suggestions from our pattern detection engine.

Your task:
1. Synthesize the data into a 2-3 sentence explanation of why the password is strong or weak
2. Review the engine's suggestions and refine them—make them more specific and actionable if possible
3. Add your own suggestions if the provided suggestions are incomplete
4. Present ALL clear, specific suggestions the user can implement immediately, ensuring none are missed.

CRITICAL INSTRUCTIONS: 
- Do not repeat raw numbers or be alarmist. 
- Use simple, everyday plain English. 
- NEVER use technical jargon like "zxcvbn", "ML model", "HIBP", "hash", or "algorithm" in your response. 
- Speak directly to the user in a friendly, conversational tone.

IMPORTANT: Format your response with suggestions on new lines like this:

[Your 2-3 sentence explanation here]

Suggestions:
- [Suggestion 1]
- [Suggestion 2]
- [Suggestion ...]"""


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
    
    suggestions_text = ""
    if payload.suggestions:
        suggestions_text = "\n- System suggestions: " + ", ".join(payload.suggestions)
    
    return f"""Password analysis:
- AI Assessment Score: {payload.strengthScore}/100
- Pattern Safety Score: {payload.zxcvbnScore}/4
- Estimated time to hack: {payload.crackTime}
- System warning: "{payload.warning}"{suggestions_text}
- Patterns detected: {_detected_patterns(payload)}
- Security rules passed: {payload.rulesPassed}/{payload.rulesTotal}
- Found in known data breaches: {breached_text}

Based on this analysis, provide your simple, jargon-free assessment and refined suggestions."""


async def stream_advice(payload: AdviseRequest) -> AsyncIterator[str]:
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = build_user_prompt(payload)

    stream = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=600,
        stream=True,
    )

    async for chunk in stream:
        text = chunk.choices[0].delta.content if chunk.choices else None
        if text:
            formatted_text = text.replace("\n", "\ndata: ")
            yield f"data: {formatted_text}\n\n"

    yield "data: [DONE]\n\n"
