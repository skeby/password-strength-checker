# generate-dataset.py
import csv
import zxcvbn as zx

with open("RockYou.txt", encoding="utf-8", errors="ignore") as src, \
     open("passwords.csv", "w", newline="") as dst:

    writer = csv.writer(dst)
    writer.writerow(["password", "guesses_log10"])

    for i, line in enumerate(src):
        pw = line.strip()
        if not pw or len(pw) > 64:
            continue
        try:
            result = zx.zxcvbn(pw)
            writer.writerow([pw, result["guesses_log10"]])
        except Exception:
            continue

        if i % 100_000 == 0:
            print(f"{i} processed...")