window.addEventListener("load", (event) => {
    StateManager.load();
});
window.addEventListener("beforeunload", (event) => {
    StateManager.save();
});
