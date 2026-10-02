import logging
from pathlib import PurePath
from os import path as os_path
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    sys_path.append(str(PurePath(__file__).parent.parent))
from registerables import Registerable, FileRegisterable, DelayedFileRegisterable, CodeRegisterable, DelayedCodeRegisterable


class JSManager:
    def __init__(self, logger_name: str = None):
        self.registered_prints: list[Registerable] = []
        self.registered_delayed_prints: list[Registerable] = []
        self.logger = None
        if logger_name:
            self.logger = logging.getLogger(logger_name)

    def register(self, value: str | PurePath, is_file: bool = False, delayed: bool = False):
        if delayed and is_file:
            if os_path.isfile(str(value)):
                self.registered_delayed_prints.append(DelayedFileRegisterable(value))
            else:
                if self.logger:
                    self.logger.error(f"{value} is not a file - file not registered!")
        elif not delayed and is_file:
            if os_path.isfile(str(value)):
                self.registered_prints.append(FileRegisterable(value))
            else:
                if self.logger:
                    self.logger.error(f"{value} is not a file - file not registered!")
        elif delayed and not is_file:
            self.registered_delayed_prints.append(DelayedCodeRegisterable(value))
        else:
            self.registered_prints.append(CodeRegisterable(value))

    def yield_print(self):
        yield f"<script>\n"
        all_prints = [*self.registered_prints, *self.registered_delayed_prints]
        for element in all_prints:
            lines = element.get().splitlines(keepends=True)
            for line in lines:
                yield line
        yield "</script>\n"

    def print(self):
        result = "<script>\n"
        all_prints = [*self.registered_prints, *self.registered_delayed_prints]
        for element in all_prints:
            result = "".join([result, element.get()])
        result = "".join([result, "</script>\n"])
        return result


if __name__ == '__main__':
    base_path_ = PurePath(__file__).parent.parent
    file1_ = PurePath(base_path_, "inputs", "_css1.css")
    file2_ = PurePath(base_path_, "inputs", "_css2.css")
    file3_ = PurePath(base_path_, "inputs", "_js1.js")
    code1_ = "let code = 'JS Code';\n"
    #
    js_manager_ = JSManager()
    js_manager_.register(file1_, True)
    js_manager_.register(file2_, True)
    js_manager_.register(file3_, True)
    js_manager_.register(code1_)
    #
    result_ = js_manager_.print()
    print(result_)
    #
    results_yield_ = ""
    for line_ in js_manager_.yield_print():
        results_yield_ = "".join([results_yield_, line_])
    print(results_yield_)
