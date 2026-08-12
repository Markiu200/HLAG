class RawModuleInstance extends ModuleInstance {
    constructor(id, module, controller) {
        super(id, module);
        this.controller = RawModuleController
    }
    open() {
        super.open();
    }
}

class RawModuleController {
    static create(module_, id_, data_, meta_) {
        let newInstance = new RawModuleInstance(id_, module_);

        let newElement = null
        let htmlEnabled = true;
        if (meta_["html"] ?? "" == "disable") {
            htmlEnabled = false;
        }

        data_.nodes.forEach(node => {
            if (node["isRef"] == 0) {
                if (htmlEnabled) {
                    newElement = document.createElement("pre");
                    newElement.style.fontFamily = "inherit";
                    newElement.style.display = "inline";
                    newElement.style.margin = 0;
                    newElement.innerHTML = node["line"];
                    newInstance.nodes.push(newElement);
                } else {
                    newElement = document.createElement("span");
                    newElement.innerText = node["line"];
                    newInstance.nodes.push(newElement);
                }
            } else {
                let nestedInstance = RefResolver.resolve(node["line"]);
                nestedInstance.nodes.forEach(n_node => {
                    newInstance.nodes.push(n_node);
                });
                newInstance.nestedInstances.push(nestedInstance);
            }
        });
        return newInstance;
    }
}

