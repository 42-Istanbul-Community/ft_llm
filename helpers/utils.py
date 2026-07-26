import random
import string
import datetime
import time

from jinja2 import Environment, FileSystemLoader


def get_jinja2(**kwargs):
    try:
        # assert hasattr(kwargs,"ENVIRONMENT"),"ENVIRONMENT parameter missing."
        path = kwargs["ENVIRONMENT"]
        name = kwargs["ENTITY"]
        # assert hasattr(kwargs,"ENTITY"),"ENTITY parameter missing."
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


def get_system_message(name=None, folder=None, extension=".txt"):
    system_message = ""
    folders = ["personas", "institude"]
    if not name:
        name = "empty"
    if not folder:
        folder = ["", "optional_roles", "unused"]
    else:
        folder = [folder] if not isinstance(folder, list) else folder
    for fold in folder:
        # file_name = "./personas",folder,name+".txt"
        for folde in folders:
            # file_name = join(f"./{folde}",fold,name+extension)
            # print(f"Seeking: {file_name}")
            for ext in [".txt", ".md", ".j2"]:
                try:
                    system_message = get_context(f"./{folde}/"+fold, name+ext)
                    # print(system_message)
                    if not system_message:
                        raise ValueError
                    # with open(file_name,"/f.read()
                except Exception as e:
                    pass
                else:
                    # print(f"./{folde}/"+fold,name+ext)
                    return system_message
    return system_message


def getFilesInDirectory(path=''):
    locations = list(walk(path))[0]
    files = locations[2]
    return files
