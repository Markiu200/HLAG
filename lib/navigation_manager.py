class NavigationManager:
    @classmethod
    def print_html(cls):
        # todo this
        yield "<nav>NAVIGATION</nav>"

    @classmethod
    def print_js_manager(cls):
        # todo this
        yield "class Navigation {}"

    @classmethod
    def print_js_data(cls):
        # todo this
        yield """let windows = [
      {id: 0, title: "Home", contents: [{module: "text", id: 0}, {module: "text", id: 2}]},
      {id: 1, title: "Data", contents: [{module: "text", id: 1}]},
      {id: 2, title: "Referenced", contents: [{module: "text", id: 3}]},
    ];"""
