class EnlinkModuleInstance extends ModuleInstance {
    constructor(id, module, controller) {
        super(id, module);
        this.controller = EnlinkModuleController
    }
}

class EnlinkModuleController {
  static create(module_, id_, data_, meta_) {
    let newInstance = new EnlinkModuleInstance(id_, module_);
    let allItems = [];
    //
    // data={"nodes": {"title": "", "link": "", "desc": "", "images": ""}}
    //
    data_.nodes.forEach(item => {  // this should be a list 
      let currentItem = document.createElement("div");
      currentItem.classList.add("enlink");
      //
      if (item["title"]) {
        let titleElement = document.createElement("h4");
        titleElement.classList.add("title");
        titleElement.innerHTML = item["title"];
        currentItem.appendChild(titleElement);
      }
      if (item["link"]) {
        let linkElement = document.createElement("a");
        linkElement.classList.add("link");
        let linkDiv = document.createElement("div");
        linkDiv.classList.add("linkDiv");
        linkDiv.appendChild(linkElement);
        linkElement.setAttribute("href", item["link"]);
        linkElement.innerText = item["link"];
        currentItem.appendChild(linkDiv);
      }
      if (item["desc"]) {
        let descElement = document.createElement("span");
        descElement.classList.add("desc");
        descElement.innerHTML = item["desc"];
        currentItem.appendChild(descElement);
      }
      if (item["images"]) {
        let imagesContainer = document.createElement("div");
        imagesContainer.classList.add("images");
        item["images"].forEach (el => {
          let imageContainer = document.createElement("img");
          imageContainer.setAttribute("src", el);
          imageContainer.classList.add("image");
          imagesContainer.appendChild(imageContainer);
        });
        currentItem.appendChild(imagesContainer);
      }
      allItems.push(currentItem);
    });
    newInstance.nodes = allItems;
    return newInstance;
  }
}
