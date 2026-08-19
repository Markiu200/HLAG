//
// Linker
// and helper classes
//

class Linker {
    //PLACEHOLDER_FOR_LINKMAP
    static registered = [];
    static open(e, link) {
        let ref = Linker.linkMap.get(link);
        //
        Linker.registered.forEach(el => {
            el(e, ref);
        });
    }
    static register(callback) {
        Linker.registered.push(callback);
    }
}

