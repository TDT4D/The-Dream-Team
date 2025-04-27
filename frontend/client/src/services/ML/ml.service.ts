/* Types */
import { TrainingStatus } from "../../types/ML";

/* Components, services & etc. */
import storage from "../storage/storage.service";

const KEYS = {
  status: "ml-status",
  size: "ml-team-size",
};

export const setML_status = (status: TrainingStatus): void => {
  if (!storage.update<TrainingStatus>(KEYS.status, (_) => status))
    storage.save<TrainingStatus>(status, KEYS.status);
};

export const getML_status = (): TrainingStatus =>
  storage.get<TrainingStatus>(KEYS.status) ?? "uninitialized";

export const getTeamSize = (): number | undefined =>
  storage.get<number>(KEYS.size);
export const setTeamSize = (size: number): void => {
  if (!storage.update<number>(KEYS.size, (_) => size))
    storage.save<number>(size, KEYS.size);
};
