//
// StateManager
//
//

class StateManager {
    static registeredStatefulEntities = [];

    static register(name_, saveMethod_, loadMethod_) {
        let isRegistered = false;
        StateManager.registeredStatefulEntities.forEach((entity) => {
            if (entity.name == name_) {
                isRegistered = true;
            }
        });
        if (isRegistered == false) {
            StateManager.registeredStatefulEntities.push({
                name: name_,
                saveMethod: saveMethod_,
                loadMethod: loadMethod_
            });
        }
    }

    static load() {
        StateManager.registeredStatefulEntities.forEach((entity) => {
            entity.loadMethod();
        });
    }

    static save() {
        StateManager.registeredStatefulEntities.forEach((entity) => {
            entity.saveMethod();
        });
    }
}

