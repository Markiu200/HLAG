class RawImageModuleInstance extends ModuleInstance {
    constructor(id, module, controller) {
        super(id, module);
        this.controller = RawImageModuleController
    }
}

class RawImageModuleController {
  static create(module_, id_, data_, meta_) {
    let newInstance = new RawImageModuleInstance(id_, module_);
    let allItems = [];
    //
    data_.nodes.forEach(item => {  // this should be a list 
      let imgElement = document.createElement("img");
      imgElement.setAttribute("src", item);
      allItems.push(imgElement);
    });
    newInstance.nodes = allItems;
    return newInstance;
  }
}
