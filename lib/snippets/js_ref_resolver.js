class RefResolver {
    // todo bede musial uwzgledni JSREF i JSDICT - jako ze slownikowe wyszukiwania at runtime beda tez potrzebne
    // dla niektorych aplikacji ( will it though? )
    // todo w dodatku uwzglednic znak specjalny zeby zapobiec przypadkowym uzyciom w kodzie
    static re = /\[\&\_JSREF\((.*?),(.*?)\)\_\&\]/;

    static contains_ref(line) {
        return (RefResolver.re).test(line);
    }

    static resolve(jsref) {
        // jezeli JSREF wyglada tak: JSREF(module,id)
        let found = jsref.match(RefResolver.re);
        if (!found) {
            return false;
        }
        let key = found[1];
        let value = found[2];
        // if (key == "mod") {
        return RefResolver.resolve_mod(key, parseInt(value))
        //}
    }

    static resolve_mod(module, id) {
        return ContentManager.getInstance(module, id);
    }
}

