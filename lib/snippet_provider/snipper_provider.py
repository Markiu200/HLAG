from assets.html_snippets import html_snippets


def get_snippet(snippet: str):
    snippet = html_snippets[snippet]
    return snippet


def yield_snippet(snippet: str):
    yield get_snippet(snippet)


def get_snippet_with_args(snippet: str, **kargs):
    snippet = html_snippets[snippet]
    return snippet.format(**kargs)


def yield_snippet_with_args(snippet: str, **kargs):
    yield get_snippet_with_args(snippet, **kargs)
