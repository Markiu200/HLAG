//
// ContentManager
// and helper classes
//

class WindowRecord {
    constructor(id, title, contents) {
        this.title = title;
        this.id = id;
        this.contents = contents;
    }
}

class NavigationButton {
    constructor(windowId, title) {
        this.windowId = windowId;
        this.button = document.createElement("button");
        this.buttonDiv = document.createElement("div");
        this.buttonDiv.appendChild(this.button);
        this.button.type = "button";
        this.button.innerHTML = title;
        this.button.style.width = "250px";
        this.button.style.height = "50px";
        this.button.addEventListener("click", this.clickEvent.bind(this));
    }

    clickEvent(e) {
        if (e.shiftKey) {
            Navigation.toggleWindow(this.windowId);
        } else {
            Navigation.switchToWindow(this.windowId);
        }
    }
}

class Navigation {
    //PLACEHOLDER_FOR_WINDOWMAP

    static requestedWindows = [];
    static navigationDiv = document.getElementById("nav");
    //
    static startpage = null;

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

    static generateNavigation() {
        Navigation.windowMap.forEach(element => {
            let button = new NavigationButton(element.id, element.title);
            Navigation.navigationDiv.appendChild(button.buttonDiv);
        });
    }

    static openLink(e, ref) {
      // check which window has the reffered instance
      let foundWindowId = 0;
      let i = 0;
      Navigation.windowMap.forEach(window => {
        let contents =  window.contents;
        contents.forEach(ref_ => {
          if (ref_["module"] == ref["module"] && ref_["id"] == ref["instance_id"]) {
            foundWindowId = i;
          }
        });
        i += 1;
      });
      // open it
      if (foundWindowId) {
        if (e.shiftKey) {
            Navigation.toggleWindow(foundWindowId);
        } else {
            Navigation.switchToWindow(foundWindowId);
        }
      }
    }

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
Linker.register((e, ref) => {Navigation.openLink(e, ref)});
Navigation.generateNavigation();
StateManager.register("Navigation", Navigation.saveState, Navigation.loadState);
Navigation.openStartpage();

