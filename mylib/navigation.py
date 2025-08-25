import os
from pathlib import Path

if __name__ == "__main__":
    from sys import path as syspath

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('./mylib/').absolute()))
    syspath.append(str(Path('./mylib/filetypes').absolute()))

from filetypes.directory import Directory
from article import Article


class Navigation:
    def __init__(self, root_directory: Directory):
        self.root_directory = root_directory
        # self.html_part = "<nav class=\"js-site-navigation\">\n  <button class=\"js-site-navigation-showall\">Show all</button>\n"
        self.html_part = '''\
<aside class="js-site-navigation site-navigation">
  <nav>
    <!-- Top bit -->
    <header>
      <p class="title">Newfluence</p>
    </header> <!-- /Top bit -->
    <section class="sidebar__wrapper">
      <!-- Actual buttons -->
      <ul class="sidebar__list list--primary">
'''
        self.js_part = ""
        self.indent = "        "
        self.level = 0

    def nestedness_class(self) -> str:
        if self.level > 0:
            return f" nav__nested--{self.level}"
        else:
            return ""

    def insert_expandable_html_button_div(self, that_article):
        self.html_part += f'{self.indent}<li class="js-for-{that_article.dom_id} js-nav-item sidebar__item{self.nestedness_class()}">\n'
        self.html_part += f'{self.indent + "  "}<div class="sidebar__link">\n'
        self.html_part += f'{self.indent + "    "}<div class="js-nav-expandable expandable icon active">\n'
        self.html_part += f'{self.indent + "      "}<svg class="expanded" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">\n'
        self.html_part += f'{self.indent + "        "}<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 9-7 7-7-7"/>\n'
        self.html_part += f'{self.indent + "      "}</svg>\n'
        self.html_part += f'{self.indent + "      "}<svg class="collapsed" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">\n'
        self.html_part += f'{self.indent + "        "}<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m9 5 7 7-7 7"/>\n'
        self.html_part += f'{self.indent + "      "}</svg>\n'
        self.html_part += f'{self.indent + "    "}</div>\n'
        self.html_part += f'{self.indent + "    "}<div class="js-nav-button text">{that_article.title}</div>\n'
        self.html_part += f'{self.indent + "  "}</div>\n'
        self.html_part += f'{self.indent}</li>\n'

    def insert_nonexpandable_html_button_div(self, that_article):
        self.html_part += f'{self.indent}<li class="js-for-{that_article.dom_id} js-nav-item sidebar__item{self.nestedness_class()}">\n'
        self.html_part += f'{self.indent + "  "}<div class="sidebar__link">\n'
        self.html_part += f'{self.indent + "    "}<div class="icon">\n'
        self.html_part += f'{self.indent + "      "}<svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">\n'
        self.html_part += f'{self.indent + "        "}<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.5 8H4m0-2v13a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-5.032a1 1 0 0 1-.768-.36l-1.9-2.28a1 1 0 0 0-.768-.36H5a1 1 0 0 0-1 1Z"/>\n'
        self.html_part += f'{self.indent + "      "}</svg>\n'
        self.html_part += f'{self.indent + "    "}</div>\n'
        self.html_part += f'{self.indent + "    "}<div class="js-nav-button text">{that_article.title}</div>\n'
        self.html_part += f'{self.indent + "  "}</div>\n'
        self.html_part += f'{self.indent}</li>\n'

    def get_html(self, directory=None) -> str:
        """Returns &lt;nav&gt;(all the navigation here)&lt;/nav&gt; as string"""

        if directory is None:
            directory = self.root_directory

        # Append button divs for each article / directory
        for node in directory.children:
            if isinstance(node, Directory):
                # Append that directory / article
                that_article = Article(node)
                # Check if it has more directories
                has_more_directories = False
                for nested_node in node.children:
                    if isinstance(nested_node, Directory):
                        has_more_directories = True
                        break
                if has_more_directories:
                    self.insert_expandable_html_button_div(that_article)
                    self.level += 1
                    self.get_html(node)
                    self.level -= 1
                else:
                    self.insert_nonexpandable_html_button_div(that_article)
        if directory is self.root_directory:
            # self.html_part += "</nav>"
            self.html_part += '''\
            </ul> <!-- /Actual buttons -->
          </section>
        </nav>
      </aside>
'''
            return self.html_part
        return ""

    def get_js(self, directory: Directory = None) -> str:
        if directory is None:
            directory = self.root_directory
        self.js_part = '''\
<script>
  // NAMESPACE SiteNavigation
  class SiteNavigation {
    static Navigation = class Navigation {
      static NavItem = class NavItem {
        constructor(buttonClass, articleId, children=null, active=false) {
          this.buttonClass = buttonClass;
          this.buttonDiv = document.getElementsByClassName(buttonClass)[0];
          this.button = this.buttonDiv.children[0].children[1];
          this.articleId = articleId;
          this.correspondingArticle = document.getElementById(articleId);
          this.active = active;
          if (active == true) {
            this.button.classList.add("active");
            this.correspondingArticle.classList.remove("hidden");
          } else {
            this.correspondingArticle.classList.add("hidden");
          }
          if (children == null) {
            this.children = [];
          } else {
            this.children = children;
          }
        } // constructor
        
        activate() {
          this.button.classList.add("active");
          this.correspondingArticle.classList.remove("hidden");
          this.active = true;
        }
        
        deactivate() {
          this.button.classList.remove("active");
          this.correspondingArticle.classList.add("hidden");
          this.active = false;
        }
      } // NavItem
      //
      constructor() { //constructor for Navigation class
        this.navigationContainer = document.querySelector(".js-site-navigation");
        this.allButtonContainers = this.navigationContainer.querySelectorAll(".js-nav-item");
        this.allButtons = this.navigationContainer.querySelectorAll(".js-nav-button");
        this.allExpandButtons = this.navigationContainer.querySelectorAll(".js-nav-expandable");
        this.showAllButton = this.navigationContainer.querySelector(".js-site-navigation-showall");
        this.navigationButtons = [
'''

        self.get_js_elements_recurse(directory, "          ")

        self.js_part += '''\
        ];
        this.isShowAll = false;
        this.displayedArticles = [];

        this.#startEventListeners();
      } // constructor

      /* Event listeners */
      #startEventListeners() {
        this.allButtons.forEach((item) => {
          item.addEventListener("click", this.navItemOnClick.bind(this));
        });
        this.allExpandButtons.forEach((item) => {
          item.addEventListener("click", this.expandButtonOnClick.bind(this));
        });
        //this.showAllButton.addEventListener("click", this.showAllButtonOnClick.bind(this));
      }

      navItemOnClick(event, list=null) {
        if (list == null) {
          list = this.navigationButtons;
        }

        for (let i = 0; i < list.length; i++) {
          if (list[i].buttonClass == event.target.parentElement.parentElement.classList[0]) {
            this.toggleArticle(list[i]);
            break;
          }
          if (list[i].children.length > 0) {
            this.navItemOnClick(event, list[i].children);
          }
        }
      }

      expandButtonOnClick(event, list=null, containerFound=false) {
        // Get the container element
        let containerElement = event.target;
        let isContainer = containerFound;
        while (!isContainer) {
          for (let i = 0; i < this.allButtonContainers.length; i++) {
            if (this.allButtonContainers[i] == containerElement) {
              isContainer = true;
              break;
            }
          }
          if (isContainer) {
            break;
          } else if (containerElement.parentElement) {
            containerElement = containerElement.parentElement
          } else {
            return;
          }
        }

        if (list == null) {
          list = this.navigationButtons;
          containerElement.children[0].children[0].classList.toggle("active");
        }

        for (let i = 0; i < list.length; i++) {
          if (list[i].buttonClass == containerElement.classList[0]) {
            this.toggleExpand(list[i]);
            break;
          }
          // if (list[i].children.length > 0) {
          //   this.expandButtonOnClick(event, list[i].children, true);
          // }
        }
      }

      showAllButtonOnClick(event) {
        this.showAllButton.classList.toggle("active");
        this.isShowAll = !this.isShowAll;
        if (this.isShowAll) {
          this.showAllArticles(this.navigationButtons);
        } else {
          this.showAllHideArticles(this.navigationButtons);
          this.showAllShowArticles(this.displayedArticles);
        }
      }

      /* Methods */
      toggleExpand(parentButton) {
        parentButton.children.forEach((item) => {
          // if (item.children > 0) {
          //   this.toggleExpand(item);
          // }
          item.buttonDiv.classList.toggle("hidden");
        });
      }

      toggleArticle(navItem) {
        if (this.isShowAll) {
          return;
        }
        if (navItem.active) {
          navItem.correspondingArticle.classList.add("hidden");
          navItem.button.classList.remove("active");
          this.displayedArticles.forEach((element, index) => {
            if (element == navItem) {
              this.displayedArticles.splice(index, 1);
            }
          });
        } else {
          navItem.correspondingArticle.classList.remove("hidden");
          navItem.button.classList.add("active");
          this.displayedArticles.push(navItem);
        }
        navItem.active = !navItem.active;
      }

      showAllHideArticles(navItemList) {
        for (let i = 0; i < navItemList.length; i++) {
          navItemList[i].deactivate()
          if (navItemList[i].children.length > 0) {
            this.showAllHideArticles(navItemList[i].children);
          }
        }
      }

      showAllShowArticles(navItemList) {
        for (let i = 0; i < navItemList.length; i++) {
          navItemList[i].activate()
        };
      }

      showAllArticles(navItemList) {
        for (let i = 0; i < navItemList.length; i++) {
          navItemList[i].activate()
          if (navItemList[i].children.length > 0) {
            this.showAllArticles(navItemList[i].children);
          }
        };
      }
    } // Navigation
  } // SiteNavigation
  // Initialize
  const siteNavigation = new SiteNavigation.Navigation();
</script>
'''
        return self.js_part

    def get_js_elements_recurse(self, directory: Directory, indent: str = None):
        for node in directory.children:
            if indent is None:
                indent = ""
            if isinstance(node, Directory):
                this_article = Article(node)
                dom_id = this_article.dom_id
                js_id = f"js-for-{dom_id}"
                if node.check_for_children_directories():
                    self.js_part += f'{indent}new SiteNavigation.Navigation.NavItem("{js_id}", "{dom_id}", [\n'
                    self.get_js_elements_recurse(node, indent + "  ")
                    self.js_part += f"{indent}]),\n"
                else:
                    self.js_part += f'{indent}new SiteNavigation.Navigation.NavItem("{js_id}", "{dom_id}"),\n'
