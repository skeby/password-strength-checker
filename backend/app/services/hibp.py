import httpx


HIBP_URL = "https://api.pwnedpasswords.com/range/{prefix}"
HIBP_USER_AGENT = "password-strength-checker/1.0"


async def check_pwned_password(
    hash_prefix: str, hash_suffix: str | None = None
) -> tuple[bool, int]:
    url = HIBP_URL.format(prefix=hash_prefix)
    headers = {"User-Agent": HIBP_USER_AGENT}
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    breach_count = 0
    aggregate_count = 0
    target = hash_suffix.upper() if hash_suffix else None

    for line in response.text.splitlines():
        if ":" not in line:
            continue
        suffix, count = line.split(":", maxsplit=1)
        parsed_count = int(count.strip())
        aggregate_count += parsed_count

        if target and suffix.strip().upper() == target:
            breach_count = parsed_count
            break

    if target:
        return breach_count > 0, breach_count

    return aggregate_count > 0, aggregate_count
