/* Types */
import { AuthToken } from "../../types/Auth";
import { ColumnType } from "../../types/Columns";
import { Label, LabelContent, LabelType } from "../../types/Label";
import { Project } from "../../types/Project";
import { Student, StudentStorageItem } from "../../types/Student";

/* Components, services & etc. */
import { callAPI, USE_SERVER } from "../api/api.service";
import { defaultStudents } from "./default-students";
import storage from "../storage/storage.service";

// TODO: Get stuff from local storage
export const checkStudentStatus = (student: Student): ColumnType => {
    student;
    return ColumnType.Applied;
}

// TODO: Request student statuses and add them to localstorage for caching
export const getStudentStatus = (student: Student): ColumnType => {
    student;

    // Gets random column type:
    const columnTypes = Object.keys(ColumnType)
      .map(n => Number.parseInt(n))
      .filter(n => !Number.isNaN(n));

    return columnTypes[Math.floor(Math.random() * columnTypes.length)];
}

export const getStudent = (id: number): Student => {
    return defaultStudents.filter(stud => stud.id === id)[0];
}

export const getStudents = (projectID: Project["id"], token: AuthToken): Promise<Student[]> => {
    return USE_SERVER ? callAPI<Student[]>(`/projects/${projectID}/students`, token) : Promise.resolve(defaultStudents);
}

export const getStudentLabels = (studentId: Student["id"], labelType: LabelType): LabelContent[] => {
    const saved = storage.get<StudentStorageItem>(`s${studentId}`);
    return saved?.labels?.filter(label => label.isType === labelType).map(label => label.contains) ?? [];
}

const labelsAreSame = (a: Label, b: Label): boolean => a.isType === b.isType && a.contains.content === b.contains.content

export const addLabelIfMissing = (studentId: Student["id"], label: Label): void => {
    const itemName = `s${studentId}`;
    const mapper = (old: StudentStorageItem) => {
        const oldLabels = old.labels?.filter(lbl => !labelsAreSame(lbl, label)) ?? [];
        return { ...old, labels: [ ...oldLabels, label] }
    }

    if (!storage.update<StudentStorageItem>(itemName, mapper)) {
        storage.save<StudentStorageItem>({ labels: [label]}, itemName);
    }
}

export const removeLabelFromStudent = (studentId: Student["id"], label: Label): void => {
    const mapper = (old: StudentStorageItem) => {
        const oldLabels = old.labels?.filter(lbl => !labelsAreSame(lbl, label)) ?? [];
        return { ...old, labels: oldLabels }
    }
    storage.update<StudentStorageItem>(`s${studentId}`, mapper);
}