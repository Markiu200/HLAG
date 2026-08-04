class EnlinkModuleInstance {
  constructor(id, nodes) {
    this.id = id
    this.nodes = nodes
    this.nestedInstances = []
  }
  open() {
    this.nestedInstances.forEach((instance) => {
      instance.open()
    })
  }

  close() {
    this.nestedInstances.forEach((instance) => {
      instance.close()
    })
  }
}

class EnlinkModuleManager {
  static name = "enlink";
  // trzymamy instancje we wlasnych klasach
  static instances = [];

  static getInstance(id) {
    let foundInstance = EnlinkModuleManager.instances.find((element) => {return element.id == id});
    if (foundInstance) {
      return foundInstance;
    } else {
      console.log("generating new instance...");
      let createdInstance = EnlinkModuleManager.createInstance(id);
      EnlinkModuleManager.instances.push(createdInstance);
      return createdInstance;
    }
  }

  static createInstance(id) {
    // todo: proper fetch from contentmanager
    let instanceJSON = registered_modules[EnlinkModuleManager.name].find((element) => {return element.id == id});
    if (!instanceJSON) {
      throw new Error("Instance ID "+id+" of "+EnlinkModuleManager.name+" module is not registered!");
    }
    let newInstance = new EnlinkModuleInstance(id, null);
    EnlinkModuleManager.generate(instanceJSON.data, instanceJSON.meta, newInstance);
    return newInstance;
  }

  static generate(data, meta, instance) {
    let allItems = [];
    //
    data.nodes.forEach(item => {  // this should be a list 
      let currentItem = document.createElement("div");
      currentItem.classList.add("enlink");
      //
      if (item["title"]) {
        let titleElement = document.createElement("h4");
        titleElement.classList.add("title");
        titleElement.innerHTML = item["title"];
        currentItem.appendChild(titleElement);
      }
      if (item["link"]) {
        let linkElement = document.createElement("a");
        linkElement.classList.add("link");
        let linkDiv = document.createElement("div");
        linkDiv.classList.add("linkDiv");
        linkDiv.appendChild(linkElement);
        linkElement.setAttribute("href", item["link"]);
        linkElement.innerText = item["link"];
        currentItem.appendChild(linkDiv);
      }
      if (item["desc"]) {
        let descElement = document.createElement("span");
        descElement.classList.add("desc");
        descElement.innerHTML = item["desc"];
        currentItem.appendChild(descElement);
      }
      allItems.push(currentItem);
    });
    instance.nodes = allItems;
  }
}
