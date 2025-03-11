/* Types */
import { AuthToken } from "../../types/Auth";
import { ColumnType } from "../../types/Columns";
import { Label, LabelContent, LabelType } from "../../types/Label";
import { Project } from "../../types/Project";
import { Student } from "../../types/Student";

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

const storageLabelsID = (studentId: Student["id"], labelType: LabelType): string => `s${studentId}l${labelType}`;

export const getStudentLabels = (studentId: Student["id"], labelType: LabelType): LabelContent[] => {
    const saved = storage.get<LabelContent[]>(storageLabelsID(studentId, labelType));
    return saved ?? [];
}

export const addLabelIfMissing = (studentId: Student["id"], label: Label): void => {
    const mapper = (old: LabelContent[]) => [...old.filter(lbl => lbl.content !== label.contains.content), label.contains];
    if (!storage.update<LabelContent[]>(storageLabelsID(studentId, label.isType), mapper)) {
        storage.save<LabelContent[]>([label.contains], storageLabelsID(studentId, label.isType));
    }
}

export const removeLabelFromStudent = (studentId: Student["id"], label: Label): void => {
    storage.update<LabelContent[]>(storageLabelsID(studentId, label.isType), (old: LabelContent[]) => old.filter(c => c.content !== label.contains.content));
}