class RawModuleInstance {
  constructor(id) {
    this.id = id
    this.nodes = []
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

class RawModuleManager {
  static name = "raw";
  // trzymamy instancje we wlasnych klasach
  static instances = [];

  static getInstance(id) {
    let foundInstance = RawModuleManager.instances.find((element) => {return element.id == id});
    if (foundInstance) {
      return foundInstance;
    } else {
      console.log("generating new instance...");
      let createdInstance = RawModuleManager.createInstance(id);
      RawModuleManager.instances.push(createdInstance);
      return createdInstance;
    }
  }

  static createInstance(id) {
    // todo: proper fetch from contentmanager
    let instanceJSON = registered_modules[RawModuleManager.name].find((element) => {return element.id == id});
    if (!instanceJSON) {
      throw new Error("Instance ID "+id+" of "+RawModuleManager.name+" module is not registered!");
    }
    let newInstance = new RawModuleInstance(id);
    RawModuleManager.generate(instanceJSON.data, instanceJSON.meta, newInstance);
    return newInstance;
  }

  static generate(data, meta, instance) {
    let root = document.createElement("div");
    data.nodes.forEach(element => {
      if (ReferenceResolver.contains_ref(element)) {
        // assuming Py part separated refs from rest of the text
        // todo more universal way
        let nestedInstance = ReferenceResolver.resolve(element);
        root.appendChild(nestedInstance.node);
        instance.nestedInstances.push(nestedInstance);
      } else {
        let newP = document.createElement("p");
        newP.innerHTML = element;
        root.appendChild(newP);
      }
    });
    instance.node = root;
  }
}
