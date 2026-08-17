import re


class TagPair:
    def __init__(self, left: set, right: set):
        self.left = left
        self.right = right


class Part:
    def __init__(self, tag: str):
        self.tag = tag

    def get_inner(self) -> str:
        return self.tag

    def get_outer(self) -> str:
        return self.tag

    def get_left(self):
        return None

    def get_right(self):
        return None

    def is_tag(self) -> bool:
        return False


class RightPart(Part):
    def __init__(self, tag: str, pair: TagPair):
        super().__init__(tag)
        self.pair = pair
        self.left_part = None
        self.stack: list[Part] = []  # tree
        self.has_tags = False
        self.inner_text = ""
        self.outer_text = ""

    def take(self, part: Part):
        if isinstance(part, RightPart) or isinstance(part, LeftPart):
            self.has_tags = True
        self.stack.append(part)

    def end(self, part: Part):
        self.left_part = part
        self.stack.reverse()
        self.inner_text = self.get_inner()
        self.outer_text = self.get_outer()

    def inner(self) -> list:
        result = []
        for part in self.stack:
            if isinstance(part, RightPart):
                result.extend(part.outer())
            else:
                result.append(part)
        return result

    def outer(self) -> list:
        result = [self.left_part]
        result.extend(self.inner())
        result.append(self)
        return result

    def get_left(self):
        return self.left_part

    def get_right(self):
        return self

    def get_outer(self) -> str:
        return "".join(str(item) for item in self.outer())

    def get_inner(self) -> str:
        return "".join(str(item) for item in self.inner())

    def is_tag(self) -> bool:
        return True

    def __str__(self):
        return self.tag


class LeftPart(Part):
    def __init__(self, tag: str, pair: TagPair):
        super().__init__(tag)
        self.pair = pair
        self.right_part = None

    def pair_with(self, right: RightPart):
        self.right_part = right

    def __str__(self):
        return self.tag


class Middle(Part):
    def __init__(self, middle: str):
        super().__init__(middle)
        self.middle = middle

    def __str__(self):
        return self.middle


class TagMatcherResult:
    def __init__(self, spliced: list):
        self.spliced = spliced
        self.spliced_expanded = []
        for part in spliced:
            if isinstance(part, RightPart):
                self.spliced_expanded.extend(part.outer())
            else:
                self.spliced_expanded.append(part)

    def get_tree(self) -> list[Part]:
        return self.spliced

    def get_expanded(self) -> list[Part]:
        return self.spliced_expanded

    def get_first_tag(self) -> Part:
        for part in self.spliced_expanded:
            if part.is_tag():
                return part


class TagMatcher:
    @classmethod
    def match(cls, string: str, tag_pairs: list[TagPair]):
        tag_set = set()
        for pair in tag_pairs:
            tag_set = tag_set.union(pair.left).union(pair.right)
        parts = cls.split(string, tag_set)
        return cls.match_list(parts, tag_pairs)

    @classmethod
    def match_list(cls, splitted_string: tuple, tag_pairs: list[TagPair]):
        # Step 1 - Prepare sets
        left_tags = set()
        right_tags = set()
        for pair in tag_pairs:
            left_tags = left_tags.union(pair.left)
            right_tags = right_tags.union(pair.right)

        # Step 2 - Prepare list
        spliced = []
        for part in splitted_string:
            if part in right_tags:
                for pair in tag_pairs:
                    if part in pair.right:
                        spliced.append(RightPart(tag=part, pair=pair))
                        break
            elif part in left_tags:
                for pair in tag_pairs:
                    if part in pair.left:
                        spliced.append(LeftPart(tag=part, pair=pair))
                        break
            else:
                spliced.append(Middle(middle=part))

        # Step 3 - Scan
        return cls._scan(spliced)

    @classmethod
    def _scan(cls, spliced_list: list):
        stack: list[Part] = []
        for part in spliced_list:
            if isinstance(part, RightPart):
                meet_left = False
                while not meet_left:
                    try:
                        looking_at = stack.pop()
                    except IndexError:
                        replacement_part = Middle(part.tag)
                        part.stack.reverse()
                        stack.extend(part.stack)  # Return everything it took
                        part = replacement_part
                        meet_left = True
                        continue
                    if isinstance(looking_at, LeftPart) and looking_at.tag in part.pair.left:
                        meet_left = True
                        looking_at.pair_with(part)
                        part.end(looking_at)
                    else:
                        part.take(looking_at)
                stack.append(part)
            else:
                stack.append(part)
        return TagMatcherResult(stack)

    @classmethod
    def split(cls, string: str, tags: set) -> tuple:
        re_pattern_mid = "|".join([re.escape(tag) for tag in tags])
        re_pattern = rf"({re_pattern_mid})"
        # re_pattern = re_pattern.replace("\\\\]", "]")
        new_splitted_string = re.split(re_pattern, string)
        return tuple(item for item in new_splitted_string if item != '')
