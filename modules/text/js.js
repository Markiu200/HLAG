class TextModuleInstance {
  constructor(id, node) {
    this.id = id
    this.node = node
    this.nestedInstances = []
  }
  open() {
    console.log("Text instance opened");
    this.nestedInstances.forEach((instance) => {
      instance.open()
    })
  }

  close() {
    console.log("Text instance closed");
    this.nestedInstances.forEach((instance) => {
      instance.close()
    })
  }
}

class TextModuleManager {
  static name = "text";
  // trzymamy instancje we wlasnych klasach
  static instances = [];

  static getInstance(id) {
    let foundInstance = TextModuleManager.instances.find((element) => {return element.id == id});
    if (foundInstance) {
      console.log("returning exisitng instance...")
      return foundInstance;
    } else {
      console.log("generating new instance...");
      let createdInstance = TextModuleManager.createInstance(id);
      TextModuleManager.instances.push(createdInstance);
      return createdInstance;
    }
  }

  static createInstance(id) {
    // todo: proper fetch from contentmanager
    let instanceJSON = registered_modules[TextModuleManager.name].find((element) => {return element.id == id});
    if (!instanceJSON) {
      throw new Error("Instance ID "+id+" of "+TextModuleManager.name+" module is not registered!");
    }
    let newInstance = new TextModuleInstance(id, null);
    TextModuleManager.generate(instanceJSON.data, instanceJSON.meta, newInstance);
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
