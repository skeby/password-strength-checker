# hash-passwords.py
#
# Hashes passwords from a CSV file to SHA-1 hex digests using concurrent
# batches. Output order matches input order. Writes one hash per line to
# the output file.
#
# Usage:
#   python hash-passwords.py
#
# Input:  backend/data/passwords.csv   (columns: password, guesses_log10)
# Output: backend/data/hashes.txt      (one SHA-1 hex digest per line)

import csv
import hashlib
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_FILE  = "backend/data/passwords.csv"
OUTPUT_FILE = "backend/data/hashes.txt"
BATCH_SIZE  = 50_000
MAX_WORKERS = None   # None = use all available CPU cores


# ---------------------------------------------------------------------------
# Worker function (runs in subprocess)
# ---------------------------------------------------------------------------

def hash_batch(batch: list[str]) -> list[str]:
    """
    Accept a list of plaintext passwords and return a list of SHA-1 hex
    digests in the same order. Encoding errors are replaced rather than
    raised so malformed rows do not kill the worker.
    """
    return [
        hashlib.sha1(pw.encode("utf-8", errors="replace")).hexdigest()
        for pw in batch
    ]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_batches(filepath: str, batch_size: int) -> list[list[str]]:
    """
    Read the password column from the CSV and return a list of batches.
    Each batch is a list of plaintext password strings.
    """
    batches: list[list[str]] = []
    current: list[str] = []

    with open(filepath, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)

        if "password" not in (reader.fieldnames or []):
            raise ValueError(
                f"CSV file '{filepath}' must have a 'password' column. "
                f"Found columns: {reader.fieldnames}"
            )

        for row in reader:
            pw = row["password"].strip()
            if not pw:
                continue
            current.append(pw)
            if len(current) >= batch_size:
                batches.append(current)
                current = []

    if current:
        batches.append(current)

    return batches


def format_duration(seconds: float) -> str:
    """Return a human-readable duration string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}m {secs}s"


def format_number(n: int) -> str:
    return f"{n:,}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # --- validate input file ------------------------------------------------
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Input file not found: '{INPUT_FILE}'\n"
            "Make sure you are running this script from the repo root and "
            "that backend/data/passwords.csv exists."
        )

    # --- load all batches into memory first so we know total count ----------
    print("Loading passwords from CSV...")
    batches = load_batches(INPUT_FILE, BATCH_SIZE)

    if not batches:
        print("No passwords found in input file. Exiting.")
        return

    total_passwords = sum(len(b) for b in batches)
    total_batches   = len(batches)
    worker_count    = MAX_WORKERS or os.cpu_count() or 1

    print(f"  Passwords  : {format_number(total_passwords)}")
    print(f"  Batches    : {format_number(total_batches)} x {format_number(BATCH_SIZE)}")
    print(f"  Workers    : {worker_count}")
    print(f"  Output     : {OUTPUT_FILE}")
    print()

    # --- ensure output directory exists ------------------------------------
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # --- submit all batches and collect results in original order -----------
    results: dict[int, list[str]] = {}
    completed_count = 0
    start_time = time.monotonic()

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
        # map future -> original batch index so we can reassemble in order
        futures = {
            pool.submit(hash_batch, batch): index
            for index, batch in enumerate(batches)
        }

        for future in as_completed(futures):
            batch_index          = futures[future]
            results[batch_index] = future.result()
            completed_count     += len(results[batch_index])

            elapsed = time.monotonic() - start_time
            pct     = (completed_count / total_passwords) * 100
            rate    = completed_count / elapsed if elapsed > 0 else 0
            eta     = (total_passwords - completed_count) / rate if rate > 0 else 0

            print(
                f"\r  {format_number(completed_count)} / {format_number(total_passwords)}"
                f"  ({pct:5.1f}%)"
                f"  {format_number(int(rate))}/s"
                f"  ETA {format_duration(eta)}   ",
                end="",
                flush=True,
            )

    print()  # newline after progress line

    # --- write output in original input order ------------------------------
    print("\nWriting hashes to output file...")
    written = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for index in range(total_batches):
            for digest in results[index]:
                out.write(digest + "\n")
                written += 1

    total_time = time.monotonic() - start_time

    print(f"  Hashes written : {format_number(written)}")
    print(f"  Time taken     : {format_duration(total_time)}")
    print(f"  Average rate   : {format_number(int(written / total_time))}/s")
    print(f"\nDone. Output saved to {OUTPUT_FILE}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()