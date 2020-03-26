export function getUrl(url:string) {
    //重写URL
    const appName = "Finance";
    if (url.startsWith("/api")) {
        if (location.pathname.startsWith("/" + appName)) {
            return `/${appName}${url}`;
        }
    }
    return url;
}