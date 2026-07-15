import re
from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade


def init():
    print("Initiating Text module...")
    module_path = PurePath(__file__).parent
    ModuleFacade.register_js(PurePath(module_path, "js.js"))


def parse(input_data):
    lines = []
    last_find = 0
    while True:
        search = re.search(r'JSREF\(.*?\)', input_data[last_find:])
        if not search:
            break
        lines.append(input_data[last_find:search.regs[0][0] - 1])
        lines.append(input_data[search.regs[0][0]:search.regs[0][1]])
        last_find = search.regs[0][1] + 1
    lines.append(input_data[last_find:])
    #
    result = {
        "module": "text",
        "content": lines,
        "metadata": ""
    }
    return result
