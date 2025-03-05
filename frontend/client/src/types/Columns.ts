/* Types */
import { Student, StudentWithLocation } from "./Student";

export enum ColumnType {
    Applied = 0,
    Potential = 1,
    Selected = 2
}

export const enum ColumnCreation {
    Initial,
    Request
}

export type StudentToColMapper = (students: Student[]) => StudentWithLocation[]