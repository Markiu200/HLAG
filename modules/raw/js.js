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
                let newPre = document.createElement("pre");
                newPre.style.fontFamily = "inherit";
                newPre.style.display = "inline";
                newPre.style.margin = 0;
                if (htmlEnabled) {
                    newPre.innerHTML = node["line"];
                    newInstance.nodes.push(newPre);
                } else {
                    newPre.innerText = node["line"];
                    newInstance.nodes.push(newPre);
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

