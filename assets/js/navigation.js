// Navigation class
class Navigation {
  // trzymamy windows z glownego
  static requestedWindows = [];

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
}
