//
// PyDocNavigation
// and helper classes
//

class PyDocNavigation {
    static NavItem = class NavItem {
        constructor(link, parent, title) {
            this.link = link
            this.parent = parent;  // NavItem parent
            this.title = title;
            this.childrenNavItems = [];
            //
            this.htmlNavItemTitle = document.createElement("div");
            this.htmlNavItemTitle.innerHTML = `<a>${this.title}</a>`;
            this.htmlNavItemArrow = document.createElement("div");
            //
            this.htmlNavItem = document.createElement("div");
            this.htmlNavItem.classList.add("nav-item");
            this.htmlNavItem.appendChild(this.htmlNavItemArrow);
            this.htmlNavItem.appendChild(this.htmlNavItemTitle);
            //
            this.htmlNavItemContainer = document.createElement("div");
            this.htmlNavItemContainer.classList.add("nav-item-container");
            this.htmlNavItemContainer.appendChild(this.htmlNavItem);
        }
    }
    //
    static Separator = class Separator extends PyDocNavigation.NavItem {
        constructor(link, parent, title) {
            super(link, parent, title);
            this.htmlNavItemTitle.classList.add("nav-item--title--separator");
            this.htmlNavItemContainer.classList.add("nav-item--separator");
        }
    }
    //
    static Leaf = class Leaf extends PyDocNavigation.NavItem {
        constructor(link, parent, title, instances) {
            super(link, parent, title);
            this.instances = instances;
            this.isActive = false;
            this.htmlNavItemTitle.classList.add("nav-item--title");
            this.htmlNavItemArrow.classList.add("nav-item--arrow");
            this.htmlNavItemArrow.innerText = String.fromCodePoint(0x25AA);
            this.htmlNavItemTitle.addEventListener("click", this.clickEvent.bind(this));
        }
        close() {
            this.isActive = false;
            this.htmlNavItem.classList.remove("active");
        }
        open() {
            this.isActive = true;
            this.htmlNavItem.classList.add("active");
            this.expandBranch();
        }
        expandBranch() {
            if (this.parent && this.parent instanceof PyDocNavigation.Branch) {
                this.parent.expand();
            }
        }
        clickEvent(e) {
            if (e.shiftKey) {
                PyDocNavigation.Navigation.toggleWindow(this);
            } else {
                PyDocNavigation.Navigation.switchToWindow(this);
            }
        }
    }
    //
    static Branch = class Branch extends PyDocNavigation.Leaf {
        constructor(link, parent, title, childrenMapEntries, instances, level) {
            super(link, parent, title, instances);
            this.childrenMapEntries = childrenMapEntries;
            this.level = level;
            //
            this.htmlNavItemChildrenContainer = document.createElement("div");
            this.htmlNavItemChildrenContainer.classList.add("nav-item-children-container");
            this.htmlNavItemChildrenContainer.style.paddingLeft = "10px";
            this.htmlNavItemContainer.appendChild(this.htmlNavItemChildrenContainer);
            //
            this.htmlNavItemArrow.innerText = String.fromCodePoint(0x1F783);;
            this.isCollapsed = false;
            this.htmlNavItemArrow.addEventListener("click", this.collapseClickEvent.bind(this));
        }
        collapse() {
            if (!this.isCollapsed) {
                this.isCollapsed = true;
                this.htmlNavItemChildrenContainer.style.display = "none";
                this.htmlNavItemArrow.innerText = String.fromCodePoint(0x1F782);;
                PyDocNavigation.Navigation.intOfCollapsedBranches += 1;
                if (PyDocNavigation.Navigation.root) {
                    PyDocNavigation.Navigation.root.updateArrow();
                }
            }
        }
        expand() {
            if (this.isCollapsed) {
                this.isCollapsed = false;
                this.htmlNavItemChildrenContainer.style.display = "flex";
                this.htmlNavItemArrow.innerText = String.fromCodePoint(0x1F783);
                PyDocNavigation.Navigation.intOfCollapsedBranches -= 1;
                if (PyDocNavigation.Navigation.root) {
                    PyDocNavigation.Navigation.root.updateArrow();
                }
            }
            if (this.parent && this.parent instanceof PyDocNavigation.Branch) {
                this.parent.expand();
            }
        }
        clickEvent(e) {
            if (e.shiftKey) {
                PyDocNavigation.Navigation.toggleWindow(this);
            } else {
                if (this.isActive && !this.isCollapsed) {
                    this.collapse();
                } else if (this.isActive && this.isCollapsed) {
                    this.expand();
                } else {
                    PyDocNavigation.Navigation.switchToWindow(this);
                }
            }
        }
        collapseClickEvent(e) {
            if (this.isCollapsed) {this.expand();} else {this.collapse();}
        }
    }
    //
    //
    static Root = class Root extends PyDocNavigation.Leaf {
        constructor(link, parent, title, instances) {
            super(link, parent, title, instances);
            this.htmlNavItemArrow.innerText = String.fromCodePoint(0x2B9E);
            this.isCollapsed = false;
            this.htmlNavItemArrow.addEventListener("click", this.collapseAllClickEvent.bind(this));
        }
        updateArrow() {
            if (PyDocNavigation.Navigation.intOfCollapsedBranches == PyDocNavigation.Navigation.intOfBranches) {
                // All branches collapsed
                this.htmlNavItemArrow.innerText = String.fromCodePoint(0x2B9E);
                this.isCollapsed = true;
            } else {
                // Some branches expanded
                this.htmlNavItemArrow.innerText = String.fromCodePoint(0x2B9F);
                this.isCollapsed = false;
            }
        }
        collapseAllClickEvent(e) {
            if (this.isCollapsed) {this.expand();} else {this.collapse();}
        }
        collapse() {
            if (!this.isCollapsed) {
                // Expand every branch;
                for (const [link, data] of PyDocNavigation.Navigation.refMap) {
                    if (data["instance"] && data["instance"] instanceof PyDocNavigation.Branch) {
                        data["instance"].collapse();
                    }
                };
                this.isCollapsed = true;
                this.updateArrow();
            }
        }
        expand() {
            if (this.isCollapsed) {
                // Collapse every branch;
                for (const [link, data] of PyDocNavigation.Navigation.refMap) {
                    if (data["instance"] && data["instance"] instanceof PyDocNavigation.Branch) {
                        data["instance"].expand();
                    }
                };
                this.isCollapsed = false;
                this.updateArrow();
            }
        }
    }
    //
    //
    //
    static SavedRequest = class SavedRequest {
        /**
         * @param {PyDocNavigation.NavItem} navItem 
         * @param {RequestedWindow} requestedWindow 
         */
        constructor(navItem, requestedWindow) {
            /** @type {PyDocNavigation.NavItem} */
            this.navItem = navItem;
            /** @type {RequestedWindow} */  // Defined at ContentManager JS
            this.requestedWindow = requestedWindow;
        }
    }
    //
    //
    //
    static Navigation = class Navigation {
        //PLACEHOLDER_FOR_MENUMAP
        /** @type {SavedRequest[]} */
        static savedRequests = [];
        static navigationDiv = document.getElementById("nav");
        static refMap = new Map();  // Each item is a representation of directory and it's direct module instances
        //
        static startpage = null;
        static intOfBranches = 0;
        static intOfCollapsedBranches = 0;
        static root = null;
        //
        // ContentManager requests
        /**
         * @param {ContentManagerWindowRequest} windowRequest 
         */
        static requestWindow(windowRequest, requestingNavItem) {
            let requestedWindow = ContentManager.openWindow(windowRequest);
            if (requestedWindow) {
                requestingNavItem.open();
                const newSavedRequest = new PyDocNavigation.SavedRequest(requestingNavItem, requestedWindow);
                return newSavedRequest;
            }
            return -1;
        }
        /**
         * @param {SavedRequest} savedRequest 
         */
        static dismissWindow(savedRequest) {
            const close_success = ContentManager.closeWindow(savedRequest.requestedWindow);
            if (close_success) {
                savedRequest.navItem.close();
                const index = Navigation.savedRequests.indexOf(savedRequest);
                return index;
            }
            return -1;
        }
        //
        // Internal state handling
        /**
         * @param {NavItem} navItem 
         */
        static toggleWindow(navItem) {
            const openedRequest = Navigation.savedRequests.find((savedRequest) => {
                    return savedRequest.navItem.link == navItem.link;
                });
            if (openedRequest) {
                const dismissedIndex = Navigation.dismissWindow(openedRequest);
                if (dismissedIndex != -1) {
                    Navigation.savedRequests.splice(dismissedIndex, 1);
                }
            } else {
                const newRequest = new ContentManagerWindowRequest(navItem.link, navItem.title, navItem.instances);
                const newSavedRequest = Navigation.requestWindow(newRequest, navItem);
                Navigation.savedRequests.push(newSavedRequest);
            }
        }
        /**
         * @param {NavItem} navItem 
         */
        static switchToWindow(navItem) {
            Navigation.savedRequests.forEach(savedRequest => {
                Navigation.dismissWindow(savedRequest);
            });
            Navigation.savedRequests.splice(0);
            const newRequest = new ContentManagerWindowRequest(navItem.link, navItem.title, navItem.instances);
            const newSavedRequest = Navigation.requestWindow(newRequest, navItem);
            Navigation.savedRequests.push(newSavedRequest);
        }
        //
        // Menu generation code
        static generateNavigation() {
            Navigation.generateNavigationRecursive(PyDocNavigation.Navigation.navigationDiv, Navigation.menuMap.entries(), null, 0);
        }
        static generateNavigationRecursive(containingHTMLElement, map, parentNavItem, level) {
            for (const [link, data] of map) {
                let navItem = null;
                // Decide between Root, Branch, Leaf, Header and Separator
                if (link == "_") {  // Root
                    navItem = new PyDocNavigation.Root(link, parentNavItem, data["title"], data["instances"]);
                    containingHTMLElement.appendChild(navItem.htmlNavItemContainer);
                    data["instance"] = navItem;
                    Navigation.root = navItem;
                }
                else if (data.children.length > 0) {  // Branch
                    navItem = new PyDocNavigation.Branch(link, parentNavItem, data["title"], data["children"], data["instances"], level);
                    Navigation.generateNavigationRecursive(navItem.htmlNavItemChildrenContainer, navItem.childrenMapEntries, navItem, level+1);
                    containingHTMLElement.appendChild(navItem.htmlNavItemContainer);
                    data["instance"] = navItem;
                    Navigation.intOfBranches += 1;
                } else if (data["type"] == "separator") {  // Separator
                    navItem = new PyDocNavigation.Separator(link, parentNavItem, data["title"]);
                    containingHTMLElement.appendChild(navItem.htmlNavItemContainer);
                    data["instance"] = navItem;
                } else {  // Leaf
                    navItem = new PyDocNavigation.Leaf(link, parentNavItem, data["title"], data["instances"]);
                    containingHTMLElement.appendChild(navItem.htmlNavItemContainer);
                    data["instance"] = navItem;
                }
                //
                if (navItem.parent) {
                    navItem.parent.childrenNavItems.push(navItem);
                }
                // Expand refMap with all module instances and menu item link pairs
                data["instances"].forEach(instance => {
                    let mix = instance["module"] + instance["id"];
                    Navigation.refMap.set(mix, {"link": link, "instance": navItem});
                });
                // Expand refMap link to link pair (redundant, but helps the algorithm)
                Navigation.refMap.set(link, {"link": link, "instance": navItem});
            }
            // After iterating over entire map, update root status
            if (level == 0 && PyDocNavigation.Navigation.root) {
                PyDocNavigation.Navigation.root.updateArrow();
            }
        }
        //
        // Link handling
        static openLink(e, link, response) {
            const hostPath = response["host"]["hostPath"];
            let item = null;
            let mapped = Navigation.refMap.get(hostPath);
            if (mapped) {  // First hit
              item = mapped["instance"];
            } else {  // Else search by Ref
              const refMix = response["host"]["hostRef"]["module"] + response["host"]["hostRef"]["id"];
              let mapped = Navigation.refMap.get(refMix);
              if (mapped) {
                item = mapped["instance"];
              }
            }
            if (item) {
                if (e.shiftKey) {
                    PyDocNavigation.Navigation.toggleWindow(item);
                } else {
                    PyDocNavigation.Navigation.switchToWindow(item);
                }
            } else {
                console.log("openLink item not found.")
            }
        }
        //
        //
        static openStartpage() {
            if (!Navigation.startpage) {
                Navigation.startpage = Navigation.refMap.get("_");
                Navigation.switchToWindow(this.startpage["instance"]);
            }
        }
        //
        // State management
        static saveState() {
            let currentlyOpenedLinks = [];
            Navigation.savedRequests.forEach(savedRequest => {
                currentlyOpenedLinks.push(savedRequest.navItem.link);
            })
            let collapseMap = [];
            for (const [link, data] of PyDocNavigation.Navigation.refMap) {
                    if (data["instance"] && data["instance"] instanceof PyDocNavigation.Branch) {
                        collapseMap.push([link, data["instance"].isCollapsed]);
                    }
                };
            const state = {
                "currentlyOpenedLinks": currentlyOpenedLinks,
                "collapseMap": collapseMap
            }
            localStorage.setItem("PyDocNavigation", JSON.stringify(state));
        }
        static loadState() {
            const loadedStateObject = JSON.parse(localStorage.getItem("PyDocNavigation"));
            if (loadedStateObject && loadedStateObject["currentlyOpenedLinks"]) {
                // close all windows
                Navigation.savedRequests.forEach(savedRequest => {
                    Navigation.dismissWindow(savedRequest);
                });
                Navigation.savedRequests.splice(0);
                // check if links are still the same
                let allOk = true;
                for (const link of loadedStateObject["currentlyOpenedLinks"]) {
                    if (!Navigation.refMap.get(link)) {
                        allOk = false;
                        console.log("Directory structure or link names changed, state not loaded.");
                        localStorage.removeItem("PyDocNavigation");
                    }
                }
                // if all ok, open saved windows
                if (allOk) {
                    Navigation.startpage = true;  // Prevents from opening default startpage
                    for (const link of loadedStateObject["currentlyOpenedLinks"]) {
                        const navItem = Navigation.refMap.get(link);
                        Navigation.toggleWindow(navItem["instance"]);
                    }
                }
                // expand or collapse Branches
                if (loadedStateObject["collapseMap"]) {
                    loadedStateObject["collapseMap"].forEach(saved => {
                        const navItem = PyDocNavigation.Navigation.refMap.get(saved[0]);  // saved[0] is "link" part
                        if (navItem && navItem["instance"] && navItem["instance"] instanceof PyDocNavigation.Branch) {
                            if (saved[1]) {  // if isCollapsed is true
                                navItem["instance"].collapse();
                            } else {
                                navItem["instance"].expand();
                            }
                        }
                    });
                }
            }
        }
    }
}
Linker.register((e, link, response) => {PyDocNavigation.Navigation.openLink(e, link, response)});
PyDocNavigation.Navigation.generateNavigation();
StateManager.register("PyDocNavigation", PyDocNavigation.Navigation.saveState, PyDocNavigation.Navigation.loadState);
PyDocNavigation.Navigation.openStartpage();

