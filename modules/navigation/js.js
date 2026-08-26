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
                let button = null;
                if (data.children.length > 0) {
                    button = new PyDocNavigation.Branch(link, data["parent"], data["title"], data["children"], data["instances"], 0);
                    Navigation.generateNavigationRecursive(button.childrenDOMElement, button.children);
                    parent.appendChild(button.twoParterDiv);
                    data["instance"] = button;
                } else {
                    button = new PyDocNavigation.NavItem(link, data["parent"], data["title"], data["children"], data["instances"], 0);
                    parent.appendChild(button.buttonDiv);
                    data["instance"] = button;
                }
                // Expand refMap with all module instances and menu item link pairs
                data["instances"].forEach(instance => {
                    let mix = instance["module"] + instance["id"];
                    Navigation.refMap.set(mix, {"link": link, "instance": button});
                });
                // Expand refMap link to link pair (redundant, but helps the algorith)
                Navigation.refMap.set(link, {"link": link, "instance": button});
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
            let currentlyOpenedLinks = []
            Navigation.savedRequests.forEach(savedRequest => {
                currentlyOpenedLinks.push(savedRequest.navItem.link);
            })
            const state = {
                "currentlyOpenedLinks": currentlyOpenedLinks
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
            }
        }
    }
}
Linker.register((e, link, response) => {PyDocNavigation.Navigation.openLink(e, link, response)});
PyDocNavigation.Navigation.generateNavigation();
StateManager.register("PyDocNavigation", PyDocNavigation.Navigation.saveState, PyDocNavigation.Navigation.loadState);
PyDocNavigation.Navigation.openStartpage();

