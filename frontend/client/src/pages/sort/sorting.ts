/* Types */
import { SortMethod, StudentSorter } from "../../types/SortMethods";
import { StudentWithRow } from "../../types/Student";


export const createStudentSorter = (method: SortMethod, reverse: boolean = false): StudentSorter => {
  const compareByNames = (a: StudentWithRow, b: StudentWithRow) => a.student.name.localeCompare(b.student.name) * (reverse ? -1 : 1)

  const sortingFunctions = {
    "default": (a: StudentWithRow, b: StudentWithRow) => a.row - b.row,
    "name": compareByNames,
    "score": (a: StudentWithRow, b: StudentWithRow) => {
      if (a.student.score === undefined || b.student.score === undefined) return compareByNames(a, b);
      return (a.student.score.score - b.student.score.score) * (reverse ? -1 : 1);
    },
    "motivation": (a: StudentWithRow, b: StudentWithRow) => {
      if (a.student.score === undefined || b.student.score === undefined) return compareByNames(a, b);
      return (a.student.score.motivation - b.student.score.motivation) * (reverse ? -1 : 1);
    },
  };

  return sortingFunctions[method];
};
