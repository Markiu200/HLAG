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

        let htmlEnabled = true;
        if (meta_["html"] ?? "" == "disable") {
            htmlEnabled = false;
        }

        data_.nodes.forEach(node => {
            if (node["isRef"] == 0) {
                let newSpan = document.createElement("span");
                if (htmlEnabled) {
                    newSpan.innerHTML = node["line"];
                    newInstance.nodes.push(newSpan);
                } else {
                    newSpan.innerText = node["line"];
                    newInstance.nodes.push(newSpan);
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

