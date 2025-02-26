import { StudentWithRow } from "./Student";

export type SortMethod = "name" | "default";

export type StudentSorter = (a: StudentWithRow, b: StudentWithRow) => number