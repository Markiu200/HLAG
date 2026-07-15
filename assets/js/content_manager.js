// ContentManager class
class WindowContainer {
  constructor(title) {
    this.window = document.createElement("div");
    this.titlebar = document.createElement("div");
    this.content = document.createElement("div");
    this.window.style.border = "1px solid black";
    this.titlebar.style.borderBottom = "1px solid black";
    this.titlebar.innerHTML = title;
    this.window.appendChild(this.titlebar);
    this.window.appendChild(this.content);
  }

  hideTitlebar() {
    this.titlebar.style.display = "none";
  }

  showTitlebar() {
    this.titlebar.style.display = "initial";
  }
}



class ContentWindow {
  constructor(id, title=null) {
    this.id = id;
    this.title = title;
    this.instances = [];
    this.window = new WindowContainer(this.title);
    // TEMPORARY
    this.window.hideTitlebar();
  }

  open() {
    let content = this.window.content;
    this.instances.forEach((instance) => {
      instance.open();
      content.appendChild(instance.node);
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
  // navigation zna zarequestowane okienka, content manager trzyma ich zawartosc (ContentWindow)
  static openedWindows = [];
  static createdWindows = [];

  static getInstance(module, id) {
    let manager = moduleMap.find((el) => {return el.name == module;});
    if (!manager) {throw new Error("Manager for module "+module+" not found.")}
    let instance = manager.manager.getInstance(id);
    if (instance) {return instance;}
    throw new Error("Module "+module+" did not return instance "+id);
  }

  static createWindow(windowJSON) {
    let newWindow = new ContentWindow(windowJSON.id, windowJSON.title);
      newWindow.title = windowJSON.title;
      windowJSON.contents.forEach((element) => {
        newWindow.instances.push(ContentManager.getInstance(element.module, element.id));
      });
    ContentManager.createdWindows.push(newWindow);
    return newWindow;
  }

  static openWindow(windowJSON) {
    let window = ContentManager.createdWindows.find((element) => {return element.id == windowJSON.id;});
    if (!window) {
      window = ContentManager.createWindow(windowJSON);
    }
    let isOpened = ContentManager.openedWindows.find((element) => {return element == window;});
    if (isOpened) {
      console.log("Window "+windowJSON.id+" appears to be already opened.");
    } else {
      window.open();
      ContentManager.openedWindows.push(window);
    }
  }

  static closeWindow(windowJSON) {
    let window = ContentManager.openedWindows.find((element) => {return element.id == windowJSON.id;});
    if (window) {
      window.close();
      let index = ContentManager.openedWindows.indexOf(window);
      ContentManager.openedWindows.splice(index, 1);
    } else {
      console.log("Window "+windowJSON.id+" appears to be already closed.");
    }
  }
}
