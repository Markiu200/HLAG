// Navigation class
class NavigationButton {
    constructor(windowId, title) {
      this.windowId = windowId;
      this.button = document.createElement("button");
      this.button.type = "button";
      this.button.innerHTML = title;
      this.button.style.width = "250px";
      this.button.style.height = "50px";
      this.button.addEventListener("click", () => {Navigation.toggleWindow(this.windowId);});
    }
}

class Navigation {
  // trzymamy windows z glownego
  static requestedWindows = [];
  static navigationDiv = document.getElementById("nav");

  static requestWindow(windowId) {
    let found = windows.find((element) => {return element.id == windowId});
    ContentManager.openWindow(found);
    Navigation.requestedWindows.push(found);
  }

  static dismissWindow(windowId) {
    let found = windows.find((element) => {return element.id == windowId});
    let index = Navigation.requestedWindows.indexOf(found);
    ContentManager.closeWindow(found);
    Navigation.requestedWindows.splice(index, 1);
  }

  static toggleWindow(windowId) {
    if (Navigation.requestedWindows.find((element) => {return element.id == windowId;})) {
      Navigation.dismissWindow(windowId);
    } else {
      Navigation.requestWindow(windowId);
    }
  }

  static generateNavigation() {
    windows.forEach(element => {
      let button = new NavigationButton(element.id, element.title);
      Navigation.navigationDiv.appendChild(button.button);
    });
  }
}
Navigation.generateNavigation();
