import re
import sys
from pathlib import PurePath
sys.path.append(str(PurePath(__file__).parent))
# Own imports
from module_facade import ModuleFacade
from txt_check import TXTCheck


def init():
    print("Initiating Text module...")
    module_path = PurePath(__file__).parent
    sys.path.append(str(PurePath(module_path, "txt_check.py")))
    ModuleFacade.register_js(PurePath(module_path, "js.js"))
    ModuleFacade.register_check(TXTCheck())


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
