const itemExists = (itemName: string): boolean => {
    return localStorage.getItem(itemName) !== null;
}

function get<T>(name: string): T | undefined {
    const item = localStorage.getItem(name);
    return item !== null ? JSON.parse(item) as T : undefined;
}

function save<T>(item: T, byName: string): boolean {
    if (itemExists(byName)) return false;
    localStorage.setItem(byName, JSON.stringify(item));
    return true;
}

function update<T>(withName: string, updateFunc: (old: T) => T): boolean {
    if (!itemExists(withName)) return false;
    localStorage.setItem(withName, JSON.stringify(
        updateFunc(get<T>(withName)!)
    ));
    return true;
}

export default { get, save, update };