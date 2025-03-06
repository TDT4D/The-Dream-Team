/* Types */
import { Student, StudentWithColumn, StudentWithLocation } from "../../types/Student";

/* Components, services & etc. */
import { checkStudentStatus, getStudentStatus } from "../../services/student/student.service";
import { ColumnCreation, StudentToColMapper } from "../../types/Columns";

type ColumnAdder = (student: Student, index?: number, array?: Student[]) => StudentWithColumn

const columnInitializer = (student: Student): StudentWithColumn => { return { student, column: checkStudentStatus(student) }};
const columnRequester = (student: Student): StudentWithColumn => { return { student, column: getStudentStatus(student) }};

const createRowAdder = () => {
    const numPerCol: Array<number> = [0, 0, 0];
    return (studentW: StudentWithColumn): StudentWithLocation => {
        const row = numPerCol[studentW.column!];
        numPerCol[studentW.column!]++;
        return { ...studentW, row };
    }
}

export const addStudentsLocations = (usecase: ColumnCreation): StudentToColMapper => {
    const locationAdder = (columnAdder: ColumnAdder) => (students: Student[]): StudentWithLocation[] => students.map(columnAdder).map(createRowAdder());
    
    switch (usecase) {
        case ColumnCreation.Initial:
            return locationAdder(columnInitializer);
        case ColumnCreation.Request:
            return locationAdder(columnRequester);
        default:
            throw new Error("Invalid column creation value!");
    }
}