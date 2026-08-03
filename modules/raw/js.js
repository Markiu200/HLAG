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
    let htmlEnabled = true;
    if (meta["html"] ?? "" == "disable") {htmlEnabled = false;}

    data.nodes.forEach(node => {
      if (node["isRef"] == 0) {
        let newSpan = document.createElement("span");
        if (htmlEnabled) {
          newSpan.innerHTML = node["line"];
          instance.nodes.push(newSpan);
        } else {
          newSpan.innerText = node["line"];
          instance.nodes.push(newSpan);
        }
      } else {
        let nestedInstance = ReferenceResolver.resolve(node["line"]);
        nestedInstance.nodes.forEach(n_node => {
          instance.nodes.push(n_node);
        });
        instance.nestedInstances.push(nestedInstance);
      }
    });
  }
}
