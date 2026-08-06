class ModuleInstance {
    constructor(id, module) {
        this.id = id;
        this.module = module;
        this.nodes = [];
        this.nestedInstances = [];
    }
    open() {
        this.nestedInstances.forEach((instance) => {
            instance.open()
        });
    }
    close() {
        this.nestedInstances.forEach((instance) => {
            instance.close()
        });
    }
    receive(message) {}
}

