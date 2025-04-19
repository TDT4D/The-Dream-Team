/* Components, services & etc. */
import storage from "../storage/storage.service";

export const setML_status = (isUp: boolean): void => { storage.update<boolean>("ml-up", _ => isUp) ? undefined : storage.save<boolean>(isUp, "ml-up") };
export const isML_up = (): boolean => storage.get<boolean>("ml-up") ?? false;

