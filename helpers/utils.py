import random
import string
import datetime
import time
from os import walk
from os.path import join
from jinja2 import Environment, FileSystemLoader


def get_jinja2(path="personas", name="empty", **kwargs):
    try:
        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(f'{name}.j2')
        system_message = template.render(**kwargs)
        return system_message
    except Exception as e:
        print("jinja2", e)
        return str(e)


def get_random_string(n=5):
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def get_random_id(n=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def get_random_digits(n=9):
    return ''.join(random.choices(string.digits, k=n))


def get_datetime():
    now = datetime.datetime.now()
    return f"{now.year}/{now.month:02d}/{now.day:02d} - {now.hour:02d}:{now.minute:02d}"


def get_timestamp():
    return int(time.time()*1000)


def get_context(folder="", name=""):
    context = ""
    file_name = join(folder, name)
    try:
        with open(file_name, "r", encoding="utf8") as f:
            context = f.read()
    except Exception:
        pass
    finally:
        return context


def get_system_message(name="empty", folder="personas", extension=".txt"):
    try:
        system_message = get_context(f"{folder}", name+extension)
        if not system_message:
            raise ValueError
    except Exception:
        pass
    return system_message


def getFilesInDirectory(path=''):
    locations = list(walk(path))[0]
    files = locations[2]
    return files
