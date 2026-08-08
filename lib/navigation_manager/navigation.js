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

    static openStartpage() {
        let raws = ContentManager.instanceDB.get("raw");
        let startpage = null;
        raws.forEach(el => {
            if (el["meta"]["startpage"]) {startpage = el["meta"]["startpage"];}
        })
        if (startpage) {
            Navigation.switchToWindow(parseInt(startpage));
        }
    }
}
Navigation.generateNavigation();
Navigation.openStartpage();

