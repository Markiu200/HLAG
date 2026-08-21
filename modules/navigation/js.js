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
        }
        createDiv() {
            let htmlElement = document.createElement("div");
            htmlElement.innerText = `Title: ${this.title} Link: ${this.link}`;
            return htmlElement;
        }
        // clickEvent(e) {
        //     if (e.shiftKey) {
        //         Navigation.toggleWindow(this.windowId);
        //     } else {
        //         Navigation.switchToWindow(this.windowId);
        //     }
        // }
    }
    //
    //
    //
    static Navigation = class Navigation {
        //PLACEHOLDER_FOR_MENUMAP
        static requestedWindows = [];
        static navigationDiv = document.getElementById("nav");
        //
        static startpage = null;
        //
        static requestWindow(windowId) {
            let found = Navigation.windowMap.get(windowId);
            ContentManager.openWindow(found);
            Navigation.requestedWindows.push(found);
        }
        static dismissWindow(windowId) {
            let found = Navigation.windowMap.get(windowId);
            let index = Navigation.requestedWindows.indexOf(found);
            ContentManager.closeWindow(found);
            Navigation.requestedWindows.splice(index, 1);
        }
        static toggleWindow(windowId) {
            if (Navigation.requestedWindows.find((element) => {
                    return element.id == windowId;
                })) {
                Navigation.dismissWindow(windowId);
            } else {
                Navigation.requestWindow(windowId);
            }
        }
        static switchToWindow(windowId) {
            Navigation.requestedWindows.forEach(element => {
                ContentManager.closeWindow(element);
            });
            Navigation.requestedWindows.splice(0)
            Navigation.requestWindow(windowId);
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
Linker.register((e, ref) => {PyDocNavigation.Navigation.openLink(e, ref)});
PyDocNavigation.Navigation.generateNavigation();
StateManager.register("Navigation", PyDocNavigation.Navigation.saveState, PyDocNavigation.Navigation.loadState);
PyDocNavigation.Navigation.openStartpage();

