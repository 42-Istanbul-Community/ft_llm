import random
import string
import datetime
import time
import os


def load_env(file_path=".env"):
    if not os.path.exists(file_path):
        return

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, val = line.split("=", 1)

            key = key.strip()
            val = val.strip().strip('"').strip("'")

            os.environ[key] = val


def get_context(folder="", name=""):
    context = ""
    file_name = os.path.join(folder, name)
    print(file_name)
    try:
        with open(file_name, "r", encoding="utf8") as f:
            context = f.read()
        print(context)
    except Exception as e:
        print(f"get_context Error: {e}")
    finally:
        return context


def get_system_message(name="empty", folder="personas", extension=".txt"):
    try:
        system_message = get_context(
            folder=folder,
            name=f"{name}{extension}")
        if not system_message:
            raise ValueError
    except Exception as e:
        print("get_system_message Error:", e)
    return system_message


def get_format(path="personas", name="empty", **kwargs):
    try:
        return get_context(path, name).format(**kwargs)
    except Exception as e:
        print(f"get_format Error: {e}")


def get_random_string(n=5):
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def get_random_id(n=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def get_random_digits(n=9):
    return ''.join(random.choices(string.digits, k=n))


def get_datetime():
    now = datetime.datetime.now()
    return f"{
        now.year}/{
            now.month: 02d}/{
                now.day: 02d} - {
                    now.hour: 02d}: {
                        now.minute: 02d}"


def get_timestamp():
    return int(time.time()*1000)
