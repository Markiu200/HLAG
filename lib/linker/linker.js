//
// Linker
// and helper classes
//

class Linker {
    //PLACEHOLDER_FOR_LINKMAP
    static registeredNavigationModules = [];
    static open(e, link) {
        let response = Linker.linkMap.get(link);
        //
        Linker.registeredNavigationModules.forEach(el => {
            el(e, link, response);
        });
    }
    static register(callback) {
        Linker.registeredNavigationModules.push(callback);
    }
}

