/* Types */
import { SortMethod, StudentSorter } from "../../types/SortMethods";
import { StudentWithRow } from "../../types/Student";

export const sortFunc = (method: SortMethod, reverse: boolean = false): StudentSorter => {
    const sortingFunctions = new Map<SortMethod, StudentSorter>([
        [
            "default", (a: StudentWithRow, b: StudentWithRow) => a.row - b.row
        ],
        [
            "name", (a: StudentWithRow, b: StudentWithRow) => a.student.name.localeCompare(b.student.name) * (reverse ? -1 : 1)
        ]
    ]);

    return sortingFunctions.get(method)!;
}