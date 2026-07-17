import re
from module_facade import ModuleFacade


class BaseReference:
    def __init__(self, begin: int, end: int):
        self.begin = begin
        self.end = end

    def __lt__(self, other: 'BaseReference'):
        return self.begin < other.begin

    def __eq__(self, other: 'BaseReference'):
        return self.begin == other.begin


class ReferenceEnd(BaseReference):
    def __init__(self, begin: int, end: int):
        super().__init__(begin, end)


class Reference(BaseReference):
    def __init__(self, begin: int, end: int, number: int, key: str, value: str, content: str):
        super().__init__(begin, end)
        self.number = number
        self.key = key
        self.value = value
        self.content = content


class AReference:
    def __init__(self, content: str, meta: dict):
        self.content = content
        self.meta = meta
        self.print = None
        self.jsref = None


def _match_refs(content: str, tag_end: int):
    # todo maybe replace it with RPN  in the future
    last_pos = tag_end
    count = 0
    # todo make that less baked in
    tag_delimiter_regex = r'\[%.*?%]'
    while True:
        reg_search = re.search(tag_delimiter_regex, content[last_pos:])
        if not reg_search:
            raise RuntimeError("Spanned module without end tag match")
        if reg_search.group() == "[%end%]":
            if count > 0:
                count -= 1
                last_pos += reg_search.regs[0][1]
                continue
            else:
                return ReferenceEnd(
                    begin=reg_search.regs[0][0] + last_pos,
                    end=reg_search.regs[0][1] + last_pos
                )
        else:
            count += 1
            last_pos += reg_search.regs[0][1]
            continue


def replace_references(content: str) -> str:
    reference_regex = r'\[%(.*?):(.*?)%]'
    #
    while True:
        reg_search = re.search(reference_regex, content)
        if not reg_search:
            break
        #
        key = reg_search.groups()[0]
        value = reg_search.groups()[1]
        #
        if key == "mod":
            new_reference = Reference(
                begin=reg_search.regs[0][0],
                end=reg_search.regs[0][1],
                number=-1,
                key=key,
                value=reg_search.groups()[1],
                content=""
            )
            end_reference = _match_refs(content, new_reference.end)
            new_reference.content = content[new_reference.end:end_reference.begin]
            new_reference.end = end_reference.end
            #
            jsref = ModuleFacade.get_content_manager().get_reference_from_data({
                "module": value,
                "content": new_reference.content
            })
            content = content.replace(content[new_reference.begin:new_reference.end], jsref)
        #
        if key == "ins":
            # todo
            pass
        #
        if key == "dict":
            # todo
            pass
    return content
