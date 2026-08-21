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
            console.log("navitem closed");
        }
        open() {
            console.log("navitem opened");
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
                Navigation.savedRequests.push(new SavedRequest(requestingNavItem, requestedWindow));
                requestingNavItem.open();
            }
        }
        static dismissWindow(windowId) {
            let found = Navigation.windowMap.get(windowId);
            let index = Navigation.requestedWindows.indexOf(found);
            ContentManager.closeWindow(found);
            Navigation.requestedWindows.splice(index, 1);
        }
        //
        // Internal state handling
        /**
         * @param {NavItem} navItem 
         */
        static toggleWindow(navItem) {
            if (Navigation.requestedWindows.find((element) => {
                    return element.id == windowId;
                })) {
                Navigation.dismissWindow(windowId);
            } else {
                Navigation.requestWindow(windowId);
            }
        }
        /**
         * @param {NavItem} navItem 
         */
        static switchToWindow(navItem) {
            Navigation.savedRequests.forEach(savedRequest => {
                ContentManager.closeWindow(savedRequest.requestedWindow);
                savedRequest.navItem.close();
            });
            Navigation.savedRequests.splice(0);
            let newRequest = new ContentManagerWindowRequest(navItem.link, navItem.title, navItem.instances);
            Navigation.requestWindow(newRequest, navItem);
        }
        //
        //
        static generateNavigation() {
            for (const [link, data] of Navigation.menuMap.entries()) {
              let button = new PyDocNavigation.NavItem(link, data["parent"], data["title"], data["children"], data["instances"], 0);
              PyDocNavigation.Navigation.navigationDiv.appendChild(button.buttonDiv);
            }
        }
        //
        //
        static openLink(e, ref) {
            // check which window has the reffered instance
            let foundWindowId = 0;
            for (let window of Navigation.windowMap) {
                let foundWindowRecord = window[1]["contents"].find((el) => {
                if (el["module"] == ref["module"] && el["id"] == ref["instance_id"]) {return true;}
                });
                if (foundWindowRecord) {
                break;
                }
                foundWindowId += 1;
            }
            // open it
            if (foundWindowId < Navigation.windowMap.size) {
                if (e.shiftKey) {
                    Navigation.toggleWindow(foundWindowId);
                } else {
                    Navigation.switchToWindow(foundWindowId);
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
// Linker.register((e, ref) => {PyDocNavigation.Navigation.openLink(e, ref)});
PyDocNavigation.Navigation.generateNavigation();
// StateManager.register("Navigation", PyDocNavigation.Navigation.saveState, PyDocNavigation.Navigation.loadState);
// PyDocNavigation.Navigation.openStartpage();

