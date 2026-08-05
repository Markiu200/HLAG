class RawImageModuleInstance {
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

class RawImageModuleManager {
  static name = "raw_image";
  // trzymamy instancje we wlasnych klasach
  static instances = [];

  static getInstance(id) {
    let foundInstance = RawImageModuleManager.instances.find((element) => {return element.id == id});
    if (foundInstance) {
      return foundInstance;
    } else {
      console.log("generating new instance...");
      let createdInstance = RawImageModuleManager.createInstance(id);
      RawImageModuleManager.instances.push(createdInstance);
      return createdInstance;
    }
  }

  static createInstance(id) {
    // todo: proper fetch from contentmanager
    let instanceJSON = registered_modules[RawImageModuleManager.name].find((element) => {return element.id == id});
    if (!instanceJSON) {
      throw new Error("Instance ID "+id+" of "+RawImageModuleManager.name+" module is not registered!");
    }
    let newInstance = new RawImageModuleInstance(id, null);
    RawImageModuleManager.generate(instanceJSON.data, instanceJSON.meta, newInstance);
    return newInstance;
  }

  static generate(data, meta, instance) {
    let allItems = [];
    //
    data.nodes.forEach(item => {  // this should be a list 
      let imgElement = document.createElement("img");
      imgElement.setAttribute("src", item);
      allItems.push(imgElement);
    });
    instance.nodes = allItems;
  }
}
