//
// ContentManager
// and helper classes
//

class WindowHTMLContainer {
    constructor(title) {
        this.window = document.createElement("div");
        this.titlebar = document.createElement("div");
        this.content = document.createElement("div");
        this.window.style.border = "1px solid black";
        this.titlebar.style.borderBottom = "1px solid black";
        this.titlebar.innerHTML = title;
        this.window.appendChild(this.titlebar);
        this.window.appendChild(this.content);
        this.window.classList.add("window-html-container")
    }

    hideTitlebar() {
        this.titlebar.style.display = "none";
    }

    showTitlebar() {
        this.titlebar.style.display = "initial";
    }
}

class ContentWindow {
    constructor(id, title) {
        this.id = id;
        this.title = title;
        this.instances = [];
        this.window = new WindowHTMLContainer(this.title);
        // TEMPORARY
        this.window.hideTitlebar();
    }
    populate() {
        let content = this.window.content;
        this.instances.forEach((instance) => {
            instance.nodes.forEach(node => {
                content.appendChild(node);
            });
        })
    }
    open() {
        this.instances.forEach((instance) => {
            instance.open();
        })
        ContentManager.main.appendChild(this.window.window);
    }
    close() {
        this.instances.forEach((instance) => {
            instance.close();
        })
        ContentManager.main.removeChild(this.window.window);
    }
}

class ContentManager {
    static main = document.getElementById("main");

    //PLACEHOLDER_FOR_INSTANCEDB

    static openedWindows = [];
    static createdWindows = [];

    //PLACEHOLDER_FOR_CONTROLLERMAP

    static getInstance(module_, id_) {
        let moduleDB = ContentManager.instanceDB.get(module_);
        let moduleEntry = moduleDB.find(el => {
            return el.id == id_;
        });
        //
        if (moduleEntry.instance != null) {
            return moduleEntry.instance;
        } else {
            let creator = ContentManager.controllerMap.get(module_);
            let newInstance = creator.create(module_, id_, moduleEntry.data, moduleEntry.meta);
            moduleEntry["instance"] = newInstance;
            return newInstance;
        }
    }
    static openWindow(windowRecord) {
        let window = ContentManager.createdWindows.find((element) => {
            return element.id == windowRecord.id;
        });
        if (!window) {
            window = ContentManager.createWindow(windowRecord);
        }
        let isOpened = ContentManager.openedWindows.find((element) => {
            return element == window;
        });
        if (!isOpened) {
            window.open();
            ContentManager.openedWindows.push(window);
        }
    }
    static createWindow(windowRecord) {
        let newWindow = new ContentWindow(windowRecord.id, windowRecord.title);
        newWindow.title = windowRecord.title;
        windowRecord.contents.forEach((element) => {
            newWindow.instances.push(ContentManager.getInstance(element.module, element.id));
        });
        newWindow.populate();
        ContentManager.createdWindows.push(newWindow);
        return newWindow;
    }
    static closeWindow(windowRecord) {
        let window = ContentManager.openedWindows.find((element) => {
            return element.id == windowRecord.id;
        });
        if (window) {
            window.close();
            let index = ContentManager.openedWindows.indexOf(window);
            ContentManager.openedWindows.splice(index, 1);
        }
    }
}

