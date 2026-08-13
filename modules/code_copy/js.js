class CodeCopyModuleInstance extends ModuleInstance {
  constructor(id, module, codeList) {
    super(id, module);
    this.controller = CodeCopyModuleController
    //
    this.codeList = codeList
    this.currentCode = "";
    this.selected = 0;
    // Create DOM elements
    this.root = document.createElement("div");
    this.testSpan1 = document.createElement("span");
    this.testSpan2 = document.createElement("button");
    this.testSpan2.innerText = "change";
    this.testSpan2.parentModule = this
    this.testSpan2.addEventListener("click", (e) => {e.target.parentModule.switchCode(1);})
    this.root.appendChild(this.testSpan1)
    this.root.appendChild(this.testSpan2)
    // Initialize defaults
    this.codeList.forEach(codeItem => {
      codeItem["variables"].forEach(variable => {
        variable["current"] = variable["default"];
      });
    });
    this.craft()
    this.update()
    this.nodes.push(this.root)
  }

  changeVariable(variable, newValue) {
    this.codeList.forEach(codeItem => {
      codeItem["variables"].forEach(var_ => {
        if (var_["variable"] == variable) {
          var_["current"] = newValue;
        }
      });
    });
    this.craft()
    this.update()
  }

  switchCode(codeNumber) {
    if (codeNumber < this.codeList.length && codeNumber >= 0) {
      this.selected = codeNumber;
    }
    this.craft()
    this.update()
  }

  craft() {
    let codeParts = this.codeList[this.selected]["code"];
    let newCode = "";
    codeParts.forEach(part => {
      if (typeof part == "number") {
        let map = this.codeList[this.selected]["variables"];
        newCode += map.get(part)["current"];
      } else {
        newCode += part;
      }
    });
    this.currentCode = newCode;
  }

  update() {
    this.testSpan1.innerText = this.currentCode;
  }
}

class CodeCopyModuleController {
  static create(module_, id_, data_, meta_) {
    let newInstance = new CodeCopyModuleInstance(id_, module_, data_["codeList"]);
    return newInstance;
  }
}

