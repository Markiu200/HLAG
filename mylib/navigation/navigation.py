class Navigation:
    def __init__(self):

    
    def get_navigation_html_as_string(self) -> str:
        """Returns &lt;nav&gt;(all the navigation here)&lt;/nav&gt; as string"""
        result = "<nav>\r\n"
        for section in self.section_list:
            if section.id == "root":
                continue
            result += f"<button onclick=\"navigation.show('{section.id}')\">{section.id}</button>"
        result += "</nav>\r\n"
        return result
    
    def get_navigation_js_as_string(self) -> str:
        # get sections map
        js_map = ""
        for section in self.section_list:
            if section.id == "root":
                continue
            js_map += f"[\"{section.id}\", document.getElementById(\"{section.id}\")],\r\n"
        # generate result
        result = """<script>
  const navigation = {
    sections: new Map([
      """ + js_map + """
    ]),
    show(section) {
      this.sections.forEach((sec) => {
        sec.style.display = "none";
        if (sec.id == section) {
          sec.style.display = "block";
        }
      });
    }
  };
</script>"""
        return result