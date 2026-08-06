class BorderedTextModuleInstance extends ModuleInstance {
    constructor(id, module, controller) {
        super(id, module);
        this.controller = BorderedTextModuleController
    }
}

class BorderedTextModuleController {
  static create(module_, id_, data_, meta_) {
    let newInstance = new BorderedTextModuleInstance(id_, module_);
    let root = document.createElement("div");
    //
    root.style.border = "1px solid black";
    data_.nodes.forEach(node => {
      if (RefResolver.contains_ref(node["line"])) {
        // assuming Py part separated refs from rest of the text
        // todo more universal way
        let nestedInstance = RefResolver.resolve(node["line"]);
        root.appendChild(nestedInstance.node);
        newInstance.nestedInstances.push(nestedInstance);
      } else {
        let newP = document.createElement("p");
        newP.innerHTML = node["line"];
        root.appendChild(newP);
      }
    });
    newInstance.nodes.push(root);
    return newInstance;
  }
}
