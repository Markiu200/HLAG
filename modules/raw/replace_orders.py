import re
from module_facade import ModuleFacade
from models import Data, Card
from tag_matcher import TagMatcher, TagPair


class BaseOrder:
    def __init__(self, begin: int, end: int):
        self.begin = begin
        self.end = end

    def __lt__(self, other: 'BaseOrder'):
        return self.begin < other.begin

    def __eq__(self, other: 'BaseOrder'):
        return self.begin == other.begin


class OrderEnd(BaseOrder):
    def __init__(self, begin: int, end: int):
        super().__init__(begin, end)


class Order(BaseOrder):
    def __init__(self, begin: int, end: int, number: int, key: str, value: str, content: str):
        super().__init__(begin, end)
        self.number = number
        self.key = key
        self.value = value
        self.content = content


def _match_tags(content: str, tag_end: int):
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
                return OrderEnd(
                    begin=reg_search.regs[0][0] + last_pos,
                    end=reg_search.regs[0][1] + last_pos
                )
        else:
            count += 1
            last_pos += reg_search.regs[0][1]
            continue


def replace_orders(card: Card) -> str:
    meta_tags = TagPair({"[%>mod:"}, {"<%]"})
    nested_item_count = 0
    new_content = ""
    #
    items = TagMatcher.match(card.content, [meta_tags]).get_tree()
    for item in items:
        if item.is_tag():
            order = item.get_inner()
            parts = order.split("=", 1)
            module_name = parts[0]
            content = parts[1]
            #
            new_meta = dict(card.meta)
            if new_meta.get("relPath"):
                new_meta["relPath"] = "_".join([new_meta["relPath"], str(nested_item_count)])
                nested_item_count += 1
            if new_meta.get("relLink"):
                new_meta.pop("relLink")
            new_meta["module"] = module_name
            order_card = Card(
                node=card.node,
                file=False,
                meta=new_meta,
                content=content
            )
            jsref = ModuleFacade.content_manager.get_ref(order_card).as_string()
            new_content = "".join([new_content, jsref])
        else:
            new_content = "".join([new_content, item.tag])
    return new_content

            # new_meta = dict(card.meta)
            # if new_meta.get("relPath"):
            #     new_meta["relPath"] = "_".join([new_meta["relPath"], str(nested_item_count)])
            #     nested_item_count += 1
            # if new_meta.get("relLink"):
            #     new_meta.pop("relLink")
            # new_meta["module"] = item.get_inner()
            # order_card = Card(
            #     node=card.node,
            #     file=False,
            #     meta=new_meta,
            #     content=new_reference.content
            # )
            # jsref = ModuleFacade.content_manager.get_ref(order_card).as_string()
            # content = content.replace(content[new_reference.begin:new_reference.end], jsref, 1)


def replace_orders2(card: Card) -> str:
    """All references should be found and replaced before parsing contents. Module
    itself should know how to recognize a reference.
    :param card: -todo- Structure containing contents and metadata of the file - it should be loaded into memory entirely.
    :return: The same content, but with JSREFs in place - ready for parsing.
    """
    content = card.content
    #
    reference_regex = r'\[%(.*?):(.*?)%]'
    nested_item_count = 0
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
            new_reference = Order(
                begin=reg_search.regs[0][0],
                end=reg_search.regs[0][1],
                number=-1,
                key=key,
                value=reg_search.groups()[1],
                content=""
            )
            end_reference = _match_tags(content, new_reference.end)
            new_reference.content = content[new_reference.end:end_reference.begin]
            new_reference.end = end_reference.end
            #
            new_meta = dict(card.meta)
            if new_meta.get("relPath"):
                new_meta["relPath"] = "_".join([new_meta["relPath"], str(nested_item_count)])
                nested_item_count += 1
            if new_meta.get("relLink"):
                new_meta.pop("relLink")
            new_meta["module"] = value
            order_card = Card(
                node=card.node,
                file=False,
                meta=new_meta,
                content=new_reference.content
            )
            jsref = ModuleFacade.content_manager.get_ref(order_card).as_string()
            content = content.replace(content[new_reference.begin:new_reference.end], jsref, 1)
        #
        if key == "ins":
            # todo
            pass
        #
        if key == "dict":
            # todo
            pass
    return content
