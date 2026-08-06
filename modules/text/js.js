class TextModuleInstance extends ModuleInstance {
    constructor(id, module, controller) {
        super(id, module);
        this.controller = TextModuleController
    }
}

class TextModuleController {
  static create(module_, id_, data_, meta_) {
    let newInstance = new TextModuleInstance(id_, module_);
    
    let root = document.createElement("div");
    data_.nodes.forEach(element => {
      if (RefResolver.contains_ref(element)) {
        // assuming Py part separated refs from rest of the text
        // todo more universal way
        let nestedInstance = RefResolver.resolve(element);
        nestedInstance.nodes.forEach(node => {
          root.appendChild(node);
        });
        instance.nestedInstances.push(nestedInstance);
      } else {
        let newP = document.createElement("p");
        newP.innerHTML = element;
        root.appendChild(newP);
      }
    });
    newInstance.nodes.push(root);
    return newInstance;
  }
}

