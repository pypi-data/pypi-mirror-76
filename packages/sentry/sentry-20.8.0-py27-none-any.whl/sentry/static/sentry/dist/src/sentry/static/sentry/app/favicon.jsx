function changeFavicon(theme) {
    var n = document.querySelector('[rel="icon"][type="image/png"]');
    if (!n) {
        return;
    }
    var path = n.href.split('/sentry/')[0];
    n.href = path + "/sentry/images/" + (theme === 'dark' ? 'favicon-dark' : 'favicon') + ".png";
}
function prefersDark() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}
function updateFavicon() {
    changeFavicon(prefersDark() ? 'dark' : 'light');
}
export function setupFavicon() {
    // Set favicon to dark on load
    if (prefersDark()) {
        changeFavicon('dark');
    }
    // Watch for changes in preferred color scheme
    window.matchMedia('(prefers-color-scheme: dark)').addListener(updateFavicon);
}
//# sourceMappingURL=favicon.jsx.map