/* Types */
import { Label, LabelContent, LabelType } from "../../types/Label";
import { Student, StudentStorageItem } from "../../types/Student";

/* Components, services & etc. */
import storage from "../storage/storage.service";

export const getStudentLabels = (
  studentId: Student["id"],
  labelType: LabelType,
): LabelContent[] => {
  const saved = storage.get<StudentStorageItem>(`s${studentId}`);
  return (
    saved?.labels
      ?.filter((label) => label.isType === labelType)
      .map((label) => label.contains) ?? []
  );
};

const labelsAreSame = (a: Label, b: Label): boolean =>
  a.isType === b.isType && a.contains.content === b.contains.content;

export const addLabelIfMissing = (
  studentId: Student["id"],
  label: Label,
): void => {
  const itemName = `s${studentId}`;
  const mapper = (old: StudentStorageItem) => {
    const oldLabels =
      old.labels?.filter((lbl) => !labelsAreSame(lbl, label)) ?? [];
    return { ...old, labels: [...oldLabels, label] };
  };

  if (!storage.update<StudentStorageItem>(itemName, mapper)) {
    storage.save<StudentStorageItem>({ labels: [label] }, itemName);
  }
};

export const removeAllLabelsByType = (
  studentId: Student["id"],
  labelType: LabelType,
): void => {
  const mapper = (old: StudentStorageItem) => {
    return {
      ...old,
      labels: old.labels?.filter((lbl) => lbl.isType !== labelType) ?? [],
    };
  };
  storage.update<StudentStorageItem>(`s${studentId}`, mapper);
};

export const removeLabelFromStudent = (
  studentId: Student["id"],
  label: Label,
): void => {
  const mapper = (old: StudentStorageItem) => {
    const oldLabels =
      old.labels?.filter((lbl) => !labelsAreSame(lbl, label)) ?? [];
    return { ...old, labels: oldLabels };
  };
  storage.update<StudentStorageItem>(`s${studentId}`, mapper);
};
