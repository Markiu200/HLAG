# Format is {"title": """snippet"""}
html_snippets = {
    "beginning": """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>""",
    "after-style": "  </head>\n  <body>",
    "ending": "  </body>\n</html>",
    "tmp-js": """function ow1() {
      Navigation.requestWindow(0);
    }
    function cw1() {
      Navigation.dismissWindow(0);
    }
    function ow2() {
      Navigation.requestWindow(2);
    }
    function cw2() {
      Navigation.dismissWindow(2);
    }""",
    "tmp-html": """<button onclick="ow1()">open window 1</button>
  <button onclick="cw1()">close window 1</button>
  <button onclick="ow2()">open window 2</button>
  <button onclick="cw2()">close window 2</button>""",
    "tmp-windows": """let windows = [
      {id: 0, title: "Home", contents: [{module: "text", id: 0}, {module: "text", id: 2}]},
      {id: 1, title: "Data", contents: [{module: "text", id: 1}]},
      {id: 2, title: "Referenced", contents: [{module: "text", id: 3}]},
    ]"""
}
