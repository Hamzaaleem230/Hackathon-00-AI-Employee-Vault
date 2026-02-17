import os
import time
from datetime import datetime

APPROVED = "Approved"
LOGS = "Logs/log.txt"

os.makedirs("Logs", exist_ok=True)

print("Watching Approved folder...")

while True:
    files = os.listdir(APPROVED)

    for f in files:
        action = f"Executed action for {f}"

        with open(LOGS, "a") as log:
            log.write(f"{datetime.now()} - {action}\n")

        os.rename(f"{APPROVED}/{f}", f"Done/{f}")

        print("Action done:", f)

    time.sleep(5)
