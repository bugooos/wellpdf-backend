import os
import time
import threading

TEMP_DIR = os.getenv(
    "WELLPDF_TEMP_DIR",
    os.path.join(os.getcwd(), "temp")
)

MAX_AGE_SECONDS = 600  # 10 minutes
SCAN_INTERVAL = 120   # check every 2 minutes


def cleanup_temp_folder():
    while True:
        try:
            now = time.time()

            if not os.path.exists(TEMP_DIR):
                time.sleep(SCAN_INTERVAL)
                continue

            for filename in os.listdir(TEMP_DIR):
                path = os.path.join(TEMP_DIR, filename)

                if not os.path.isfile(path):
                    continue

                age = now - os.path.getmtime(path)

                if age > MAX_AGE_SECONDS:
                    try:
                        os.remove(path)
                    except Exception:
                        pass

        except Exception:
            pass

        time.sleep(SCAN_INTERVAL)


def start_temp_cleanup():
    thread = threading.Thread(
        target=cleanup_temp_folder,
        daemon=True
    )
    thread.start()
