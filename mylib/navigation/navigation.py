import os
from pathlib import Path

if __name__ == "__main__":
    from sys import path as syspath

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('./mylib/').absolute()))
    syspath.append(str(Path('./mylib/filetypes').absolute()))

from directory import Directory
from article import Article


class Navigation:
    def __init__(self, root_directory: Directory):
        self.root_directory = root_directory
        self.html_part = ""
        self.js_part = ""
    
    def get_html(self, directory=None, level=0) -> str:
        """Returns &lt;nav&gt;(all the navigation here)&lt;/nav&gt; as string"""
        nest_level = level
        if directory is None:
            directory = self.root_directory
        # Open nav element and put the show all button in
        if self.html_part == "":
            self.html_part = '''\

<nav class="js-site-navigation">
  <button class="js-site-navigation-showall">Show all</button>
'''
        # Append button divs for each article / directory
        for node in directory.children:
            if isinstance(node, Directory):
                # Append that directory / article
                that_article = Article(node)
                if len(node.children) > 0:
                    spacer_class = "nav_button_expand js-nav-expandable"
                else:
                    spacer_class = "nav_button_nonexpandable_spacing"
                if nest_level > 0:
                    nestness_class = f"nav__nested--{nest_level}"
                else:
                    nestness_class = ""

                self.html_part += '''\
  <div class="'''+that_article.dom_id+''' nav_button_item '''+nestness_class+'''">
    <div class='''+spacer_class+'''></div><button class="js-nav-button">'''+that_article.title+'''</button>
  </div>
'''
                # Then look for nested articles
                if len(node.children) > 0:
                    nest_level += 1
                    self.get_html(node, nest_level)
        self.html_part += "</nav>"
        return self.html_part

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
          this.button = this.buttonDiv.children[1];
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
      } // NavItem
      //
      constructor() { //constructor for Navigation class
        this.navigationContainer = document.querySelector(".js-site-navigation");
        this.allButtons = this.navigationContainer.querySelectorAll(".js-nav-button");
        this.allExpandButtons = this.navigationContainer.querySelectorAll(".js-nav-expandable");
        this.showAllButton = this.navigationContainer.querySelector(".js-site-navigation-showall");
        this.navigationButtons = ['''

        self.get_js_elements_recurse(directory)

        self.js_part += '''\
          ]),
          new SiteNavigation.Navigation.NavItem("js-for-032_active_directory", "032_active_directory", [
            new SiteNavigation.Navigation.NavItem("js-for-032_active_directory-010_ad_groups", "032_active_directory-010_ad_groups")
          ]),
        ];
        this.isShowAll = false;
        this.displayedArticles = [this.navigationButtons[0]];

        this.#startEventListeners();
      } // constructor

      /* Event listeners */
      #startEventListeners() {
        this.allButtons.forEach((item) => {
          item.addEventListener("click", this.navItemOnClick.bind(this), true);
        });
        this.allExpandButtons.forEach((item) => {
          item.addEventListener("click", this.expandButtonOnClick.bind(this), true);
        });
        this.showAllButton.addEventListener("click", this.showAllButtonOnClick.bind(this));
      }

      navItemOnClick(event, list=null) {
        if (list == null) {
          list = this.navigationButtons;
        }

        for (let i = 0; i < list.length; i++) {
          if (list[i].buttonClass == event.target.parentElement.classList[0]) {
            this.toggleArticle(list[i]);
            break;
          }
          if (list[i].children.length > 0) {
            this.navItemOnClick(event, list[i].children);
          }
        }
      }

      expandButtonOnClick(event, list=null) {
        if (list == null) {
          list = this.navigationButtons;
          event.target.classList.toggle("active");
        }

        for (let i = 0; i < list.length; i++) {
          if (list[i].buttonClass == event.target.parentElement.classList[0]) {
            this.toggleExpand(list[i]);
            break;
          }
          if (list[i].children.length > 0) {
            this.expandButtonOnClick(event, list[i].children);
          }
        }
      }

      showAllButtonOnClick(event) {
        this.showAllButton.classList.toggle("active");
        this.isShowAll = !this.isShowAll;
        if (this.isShowAll) {
          this.showAllShowArticles(this.navigationButtons);
        } else {
          this.showAllHideArticles(this.navigationButtons);
          this.showAllShowArticles(this.displayedArticles);
        }
      }

      /* Methods */
      toggleExpand(parentButton) {
        parentButton.children.forEach((item) => {
          if (item.children > 0) {
            this.toggleExpand(item);
          }
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
          navItemList[i].correspondingArticle.classList.add("hidden");
          navItemList[i].button.classList.remove("active");
          if (navItemList[i].children.length > 0) {
            this.showAllHideArticles(navItemList[i].children);
          }
        }
      }

      showAllShowArticles(navItemList) {
        for (let i = 0; i < navItemList.length; i++) {
          navItemList[i].correspondingArticle.classList.remove("hidden");
          navItemList[i].button.classList.add("active");
          if (navItemList[i].children.length > 0) {
            this.showAllShowArticles(navItemList[i].children);
          }
        };
      }
    } // Navigation
  } // SiteNavigation
  // Initialize
  const siteNavigation = new SiteNavigation.Navigation();
</script>'''
        return self.js_part

    def get_js_elements_recurse(self, directory: Directory, level: str = None):
        for node in directory.children:
            if level is None:
                level = ""
            if isinstance(node, Directory):
                this_article = Article(node)
                dom_id = this_article.dom_id
                js_id = f"js-for-{dom_id}"
                result = ""
                if len(node.children) > 0:
                    result += f'{level}new SiteNavigation.Navigation.NavItem("{js_id}", "{dom_id}", ['
                    self.get_js_elements_recurse(node, level + "  ")
                else:
                    result += f'{level}new SiteNavigation.Navigation.NavItem("{js_id}", "{dom_id}"),'
                if level != "":
                    result += "\r\n]),"
