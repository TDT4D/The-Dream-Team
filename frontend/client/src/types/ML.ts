export type TrainingStatus =
  | "uninitialized"
  | "error"
  | "initialized"
  | "loading";

export type ML_initType = "basic" | "advanced";

export type MLContextType = {
  ml_type: ML_initType;
  status: TrainingStatus;
  setStatus: (newStatus: TrainingStatus) => void;
  teamSize: number;
  setTeamSize: (newSize: number) => void;
};
