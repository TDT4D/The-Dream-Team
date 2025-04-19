import { StudentWithRow } from "./Student";

export type SortMethod = "name" | "default" | "score" | "motivation";

export type StudentSorter = (a: StudentWithRow, b: StudentWithRow) => number;
