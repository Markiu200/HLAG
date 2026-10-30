import logging
from pathlib import PurePath
from os import path as os_path
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.registerables import Registerable, FileRegisterable, DelayedFileRegisterable, CodeRegisterable, DelayedCodeRegisterable


class CodeBlock:
    def __init__(self, block_start: str, block_end: str, logger_name: str = None):
        self.block_start = block_start
        self.block_end = block_end
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
        yield f"{self.block_start}\n"
        all_prints = [*self.registered_prints, *self.registered_delayed_prints]
        for element in all_prints:
            lines = element.get().splitlines(keepends=True)
            for line in lines:
                yield line
        yield f"{self.block_end}\n"

    def print(self):
        result = f"{self.block_start}\n"
        all_prints = [*self.registered_prints, *self.registered_delayed_prints]
        for element in all_prints:
            result = "".join([result, element.get()])
        result = "".join([result, f"{self.block_end}\n"])
        return result


if __name__ == '__main__':
    base_path_ = PurePath(__file__).parent.parent
    file1_ = PurePath(base_path_, "inputs", "_css1.css")
    file2_ = PurePath(base_path_, "inputs", "_css2.css")
    file3_ = PurePath(base_path_, "inputs", "_js1.js")
    code1_ = "let code = 'JS Code';\n"
    #
    js_manager_ = CodeBlock("<codeblock>", "</codeblock>")
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
