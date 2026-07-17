class BorderedTextModuleInstance {
  constructor(id, node) {
    this.id = id
    this.node = node
    this.nestedInstances = []
  }
  open() {
    console.log("BorderedText instance opened");
    this.nestedInstances.forEach((instance) => {
      instance.open()
    })
  }

  close() {
    console.log("BorderedText instance closed");
    this.nestedInstances.forEach((instance) => {
      instance.close()
    })
  }
}

class BorderedTextModuleManager {
  static name = "bordered_text";
  // trzymamy instancje we wlasnych klasach
  static instances = [];

  static getInstance(id) {
    let foundInstance = BorderedTextModuleManager.instances.find((element) => {return element.id == id});
    if (foundInstance) {
      console.log("returning exisitng instance...")
      return foundInstance;
    } else {
      console.log("generating new instance...");
      let createdInstance = BorderedTextModuleManager.createInstance(id);
      BorderedTextModuleManager.instances.push(createdInstance);
      return createdInstance;
    }
  }

  static createInstance(id) {
    // todo: proper fetch from contentmanager
    let instanceJSON = registered_modules[BorderedTextModuleManager.name].find((element) => {return element.id == id});
    if (!instanceJSON) {
      throw new Error("Instance ID "+id+" of "+BorderedTextModuleManager.name+" module is not registered!");
    }
    let newInstance = new BorderedTextModuleInstance(id, null);
    BorderedTextModuleManager.generate(instanceJSON.data, instanceJSON.meta, newInstance);
    return newInstance;
  }

  static generate(data, meta, instance) {
    let root = document.createElement("div");
    root.style.border = "1px solid black";
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
