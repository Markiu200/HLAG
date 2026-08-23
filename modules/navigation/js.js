//
// PyDocNavigation
// and helper classes
//

class PyDocNavigation {
    static NavItem = class NavItem {
        constructor(link, parent, title, children, instances, level) {
            this.link = link
            this.parent = parent;
            this.title = title;
            this.children = children;
            this.instances = instances;
            this.level = level;
            this.buttonDiv = this.createDiv()
            this.buttonDiv.addEventListener("click", this.clickEvent.bind(this));
        }
        createDiv() {
            let htmlElement = document.createElement("div");
            htmlElement.innerText = `Title: ${this.title} Link: ${this.link}`;
            return htmlElement;
        }
        close() {
            // console.log("navitem closed");
        }
        open() {
            // console.log("navitem opened");
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
    static Branch = class Branch extends PyDocNavigation.NavItem {
        constructor(link, parent, title, children, instances, level) {
            super(link, parent, title, children, instances, level);
            this.twoParterDiv = document.createElement("div");
            this.twoParterDiv.appendChild(this.buttonDiv);
            this.childrenDOMElement = document.createElement("div");
            this.twoParterDiv.appendChild(this.childrenDOMElement);
        }
    }
    //
    //
    //
    static SavedRequest = class SavedRequest {
        /**
         * @param {NavItem} navItem 
         * @param {RequestedWindow} requestedWindow 
         */
        constructor(navItem, requestedWindow) {
            /** @type {NavItem} */
            this.navItem = navItem;
            /** @type {RequestedWindow} */
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
        //
        static startpage = null;
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
            Navigation.generateNavigationRecursive(PyDocNavigation.Navigation.navigationDiv, Navigation.menuMap.entries())
        }
        static generateNavigationRecursive(parent, map) {
            for (const [link, data] of map) {
              if (data.children.length > 0) {
                let button = new PyDocNavigation.Branch(link, data["parent"], data["title"], data["children"], data["instances"], 0);
                Navigation.generateNavigationRecursive(button.childrenDOMElement, button.children);
                parent.appendChild(button.twoParterDiv);
              } else {
                let button = new PyDocNavigation.NavItem(link, data["parent"], data["title"], data["children"], data["instances"], 0);
                parent.appendChild(button.buttonDiv);
              }
            }
        }
        //
        // Link handling
        static openLink(e, link, ref) {
            const navItem = Navigation.menuMap.get(link);
            if (navItem) {
                if (e.shiftKey) {
                    PyDocNavigation.Navigation.toggleWindow(navItem);
                } else {
                    PyDocNavigation.Navigation.switchToWindow(navItem);
                }
            }
        }
        //
        //
        static openStartpage() {
            if (!Navigation.startpage) {
                let raws = ContentManager.instanceDB.get("raw");
                
                raws.forEach(el => {
                    if (el["meta"]["startpage"]) {Navigation.startpage = el["meta"]["startpage"];}
                })
                if (Navigation.startpage) {
                    Navigation.switchToWindow(parseInt(Navigation.startpage));
                }
            }
        }
        static saveState() {
            let requestedWindows = []
            Navigation.requestedWindows.forEach(el => {
                requestedWindows.push(el.id);
            })
            const state = {
                "requestedWindows": requestedWindows
            }
            localStorage.setItem("Navigation", JSON.stringify(state));
        }
        static loadState() {
            const loadedStateObject = JSON.parse(localStorage.getItem("Navigation"));
            if (loadedStateObject && loadedStateObject["requestedWindows"]) {
                // close all windows
                Navigation.requestedWindows.forEach(element => {
                    ContentManager.closeWindow(element);
                });
                Navigation.requestedWindows.splice(0)
                // open saved ones
                loadedStateObject["requestedWindows"].forEach(el => {
                    Navigation.toggleWindow(parseInt(el));
                })
            }
        }
    }
}
Linker.register((e, ref) => {PyDocNavigation.Navigation.openLink(e, ref)});
PyDocNavigation.Navigation.generateNavigation();
// StateManager.register("Navigation", PyDocNavigation.Navigation.saveState, PyDocNavigation.Navigation.loadState);
// PyDocNavigation.Navigation.openStartpage();

