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
        self.html_part = '''\
<aside class="js-site-navigation site-navigation">
  <nav>
    <!-- Top bit -->
    <header>
      <p class="title">Newfluence</p>
    </header> <!-- /Top bit -->
    <section class="sidebar__wrapper">
      <!-- Show all button-->
      <div class="nav__steering_wrapper">
        <div class="js-site-navigation-showall nav__steering_item">Show all</div>
      </div> <!-- /Show all button-->
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
        self.html_part += f'{self.indent}<li class="sidebar__item">\n'
        self.html_part += f'{self.indent + "  "}<div class="js-for-{that_article.dom_id} js-nav-item sidebar__link{self.nestedness_class()}">\n'
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
        self.html_part += f'{self.indent}<li class="sidebar__item">\n'
        self.html_part += f'{self.indent + "  "}<div class="js-for-{that_article.dom_id} js-nav-item sidebar__link{self.nestedness_class()}">\n'
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
        constructor(jsForClassName, articleId, children=null) {
          this.jsForClassName = jsForClassName;
          this.articleId = articleId;
          this.containerElement = document.getElementsByClassName(jsForClassName)[0];
          this.correspondingArticle = document.getElementById(articleId);
          this.titleElement = this.containerElement.children[1];
          this.iconElement = this.containerElement.children[0];
          if (children == null) {
            this.children = [];
          } else {
            this.children = children;
          }
          this.active = false;
          this.deactivate();
        } // constructor
        
        activate() {
          this.titleElement.classList.add("active");
          this.correspondingArticle.classList.remove("hidden");
          this.active = true;
        }
        
        deactivate() {
          this.titleElement.classList.remove("active");
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
        this.navigationElementsTree = [
'''

        self.get_js_elements_recurse(directory, "          ")

        self.js_part += '''\
        ];
        this.allNavItems = [];
        this.allCollapsibles = [];
        // to be saved as a state
        this.isShowAll = false;
        this.checkedArticles = [];
        this.collapsedNavItems = []; // as all are assumed uncollapsed at start (by default)
        //
        this.#startEventListeners();
        this.#getAllNavItems(this.navigationElementsTree);
        this.#getAllCollapsibles();
      } // constructor

      /* contructor single use methods */
      #getAllNavItems(navItemList) {
        navItemList.forEach((navItem) => {
          this.allNavItems.push(navItem);
          if (navItem.children.length > 0) {
            this.#getAllNavItems(navItem.children);
          }
        });
      }
      //
      #getAllCollapsibles() {
        this.allNavItems.forEach((navItem) => {
          if (navItem.children.length > 0) {
            this.allCollapsibles.push(navItem);
          }
        });
      }

      /* Event listeners */
      #startEventListeners() {
        this.allButtons.forEach((item) => {
          item.addEventListener("click", this.navItemOnClick.bind(this));
        });
        this.allExpandButtons.forEach((item) => {
          item.addEventListener("click", this.expandButtonOnClick.bind(this));
        });
        this.showAllButton.addEventListener("click", this.showAllButtonOnClick.bind(this));
      }
      //
      navItemOnClick(event) {
        let navItemElement = this.findButtonByJsClassName(event.target.parentElement.classList[0]);
        if (!navItemElement) {
          throw new Error("Pressed navigation item is not found in a list of registered navItems.");
        }
        this.toggleArticle(navItemElement);
      }
      //
      expandButtonOnClick(event) {
        // Get the container element (it should have 'js-for' class in it)
        let containerElement = event.target;
        while (!containerElement.classList.contains("js-nav-item")) {
          containerElement = containerElement.parentElement; // "js-nav-item has also js-for at classList[0]"
        }
        // When element is found
        let navItemElement = this.findButtonByJsClassName(containerElement.classList[0]);
        this.toggleExpand(navItemElement);
      }
      //
      showAllButtonOnClick(event) {
        this.toggleShowAll();
      }

      /* Methods */
      // utility methods
      findButtonByJsClassName(className, navButtonList_=null) {
        let navButtonList = null;
        if (navButtonList_ != null) {
          navButtonList = navButtonList_;
        } else {
          navButtonList = this.navigationElementsTree;
        }
        let found = null;
        for (let i = 0; i < navButtonList.length; i++) {
          if (navButtonList[i].jsForClassName == className) {
            return navButtonList[i];
          }
          if (navButtonList[i].children.length > 0) {
            found = this.findButtonByJsClassName(className, navButtonList[i].children)
            if (found != null) {
              return found;
            }
          }
        }
        return found;
      }

      // related to handling expand tree part of navItems
      toggleExpand(navItem) {
        if (this.collapsedNavItems.includes(navItem)) {
          this.collapsedNavItems.forEach((element, index) => {
            if (element == navItem) {
              this.collapsedNavItems.splice(index, 1);
            }
          });
        } else {
          this.collapsedNavItems.push(navItem);
        }
        this.renderPage();
      }
      //
      collapseAllCollapsibles() {
        this.allCollapsibles.forEach((navItem) => {
          navItem.iconElement.classList.remove("active");
          navItem.children.forEach((el) => {
            el.containerElement.parentElement.classList.add("hidden");
          });
        });
      }
      //
      expandNonCollapsed(navItemList_=null) {
        let navItemList = null;
        if (navItemList_ != null) {navItemList = navItemList_;} else {navItemList = this.navigationElementsTree;}
        navItemList.forEach((navItem) => {
          navItem.containerElement.parentElement.classList.remove("hidden");
          if (navItem.children.length > 0 && this.collapsedNavItems.includes(navItem) == false) {
            navItem.iconElement.classList.add("active");
            this.expandNonCollapsed(navItem.children);
          }
        });
      }

      // related to pressing navItems title parts
      toggleArticle(navItem) {
        if (this.isShowAll) {
          return;
        }
        if (this.checkedArticles.includes(navItem)) {
          this.checkedArticles.forEach((element, index) => {
            if (element == navItem) {
              this.checkedArticles.splice(index, 1);
            }
          });
        } else {
          this.checkedArticles.push(navItem);
        }
        this.renderPage();
      }

      // related to 'Show all' button
      toggleShowAll() {
        this.showAllButton.classList.toggle("active");
        this.isShowAll = !this.isShowAll;
        if (this.isShowAll) {
          this.showAllArticles(this.navigationElementsTree);
        } else {
          this.hideAllArticles(this.navigationElementsTree);
          this.showAllSavedArticles(this.checkedArticles);
        }
      }
      //
      hideAllArticles(navItemList) {
        for (let i = 0; i < navItemList.length; i++) {
          navItemList[i].deactivate()
          if (navItemList[i].children.length > 0) {
            this.hideAllArticles(navItemList[i].children);
          }
        }
      }
      //
      showAllSavedArticles(navItemList) {
        for (let i = 0; i < navItemList.length; i++) {
          navItemList[i].activate()
        };
      }
      //
      showAllArticles(navItemList) {
        for (let i = 0; i < navItemList.length; i++) {
          navItemList[i].activate()
          if (navItemList[i].children.length > 0) {
            this.showAllArticles(navItemList[i].children);
          }
        };
      }

      // related to refreshing nav
      renderPage() {
        // Deactivate all navItems and activate only checked ones
        if (this.isShowAll == false) {
          this.allNavItems.forEach((navItem) => {
            navItem.deactivate();
          });
          this.checkedArticles.forEach((navItem) => {
            navItem.activate();
          });
        }
        // Handling collapsibles
        this.collapseAllCollapsibles();
        this.expandNonCollapsed();
      }

      /* State */
      saveState() {
        let checkedArticlesStrings = [];
        this.checkedArticles.forEach((navItem) => {
          checkedArticlesStrings.push(navItem.jsForClassName);
        });
        let collapsedNavItemsStrings = [];
        this.collapsedNavItems.forEach((navItem) => {
          collapsedNavItemsStrings.push(navItem.jsForClassName);
        });
        const stateObject = {
          isShowAll: this.isShowAll,
          checkedArticlesStrings: checkedArticlesStrings,
          collapsedNavItemsStrings: collapsedNavItemsStrings
        }
        console.log(stateObject);
        localStorage.setItem("siteNavigation", JSON.stringify(stateObject));
      }
      //
      loadState() {
        const loadedStateObject = JSON.parse(localStorage.getItem("siteNavigation"));
        console.log(loadedStateObject);
        // checked articles
        this.checkedArticles = [];
        loadedStateObject.checkedArticlesStrings.forEach((jsName) => {
          this.checkedArticles.push(this.findButtonByJsClassName(jsName));
        });
        // collapsed NavItems
        this.collapsedNavItems = [];
        loadedStateObject.collapsedNavItemsStrings.forEach((jsName) => {
          this.collapsedNavItems.push(this.findButtonByJsClassName(jsName));
        });
        //
        this.renderPage();
        if (this.isShowAll != loadedStateObject.isShowAll) {
          this.isShowAll = !loadedStateObject.isShowAll;
          this.toggleShowAll();
        }
      }
    } // Navigation
  } // SiteNavigation namespace
  // Initialize
  const siteNavigation = new SiteNavigation.Navigation();
  stateManager.register(
    "siteNavigation", 
    siteNavigation.saveState.bind(siteNavigation), 
    siteNavigation.loadState.bind(siteNavigation)
  );
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
