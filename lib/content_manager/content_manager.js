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

class ContentManagerWindowRequest {
    constructor(id, title, instances) {
        this.id = id;
        this.title = title;
        this.instances = instances;
    }
}

class RequestedWindow {
    constructor(id, window) {
        this.id = id;
        this.window = window;
    }
}

class ContentManager {
    static main = document.getElementById("main");

    //PLACEHOLDER_FOR_INSTANCEDB

    /** @type {RequestedWindow[]} */
    static openedWindows = [];  // Holds RequestedWindow items
    /** @type {RequestedWindow[]} */
    static createdWindows = [];  // Holds RequestedWindow items

    //PLACEHOLDER_FOR_CONTROLLERMAP

    static getInstance(module_, id_) {
        let moduleDB = ContentManager.instanceDB.get(module_);
        if (!moduleDB) {
            console.log(`Unable to find module: ${module_}!`);
            return false;
        }
        let moduleEntry = moduleDB.find(el => {
            return el.id == id_;
        });
        if (!moduleEntry) {
            console.log(`Unable to find id: ${id_} of module ${module_}!`);
            return false;
        }
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
    /**
     * @param {ContentManagerWindowRequest} windowRequest 
     */
    static openWindow(windowRequest) {
        let requestedWindow = ContentManager.createdWindows.find((created) => {
            return created.id == windowRequest.id;
        });
        if (!requestedWindow) {
            requestedWindow = ContentManager.createWindow(windowRequest);
            if (!requestedWindow) {
                return false;
            }
        }
        let isOpened = ContentManager.openedWindows.find((opened) => {
            return opened.id == windowRequest.id;
        });
        if (!isOpened) {
            requestedWindow.window.open();
            ContentManager.openedWindows.push(requestedWindow);
        }
        return requestedWindow;
    }
    /**
     * @param {ContentManagerWindowRequest} windowRequest 
     */
    static createWindow(windowRequest) {
        let newWindow = new ContentWindow(windowRequest.id, windowRequest.title);
        newWindow.title = windowRequest.title;
        windowRequest.instances.forEach((ref) => {
            newWindow.instances.push(ContentManager.getInstance(ref.module, ref.id));
        });
        newWindow.populate();
        let requestedWindow = new RequestedWindow(windowRequest.id, newWindow);
        ContentManager.createdWindows.push(requestedWindow);
        return requestedWindow;
    }
    /**
     * @param {RequestedWindow} requestedWindow 
     */
    static closeWindow(requestedWindow) {
        let openedWindowRequest = ContentManager.openedWindows.find((opened) => {
            return opened.id == requestedWindow.id;
        });
        if (openedWindowRequest) {
            openedWindowRequest.window.close();
            const index = ContentManager.openedWindows.indexOf(openedWindowRequest);
            if (index != -1) {
                ContentManager.openedWindows.splice(index, 1);
            }
            return true;
        }
        return false;
    }
}

