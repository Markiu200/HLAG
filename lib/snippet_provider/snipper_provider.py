from assets.html_snippets import html_snippets


def get_snippet(snippet: str, **kargs):
    snippet = html_snippets[snippet]
    return snippet.format(**kargs)


def yield_snippet(snippet: str, **kargs):
    yield get_snippet(snippet, **kargs)
