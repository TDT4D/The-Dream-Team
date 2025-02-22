/* Types */
import { Student } from "../../types/Student";

const students: Array<Student>  = [
    {
        id: 0,
        name: "Student Test0",
        labels: [
            "x"
        ],
    },
    {
        id: 1,
        name: "Student Test1",
        labels: [
            "x", "y"
        ],
    },
    {
        id: 2,
        name: "Student Test2",
        labels: [
            "y"
        ],
    },
    {
        id: 3,
        name: "Student Test3",
        labels: [
            "x", "z"
        ],
    },
    {
        id: 4,
        name: "Student Test4",
        labels: [
            "x", "y", "z"
        ],
    },
]

export const getStudentStatus = (id: number): number => {
    return +id < 3 ? 0 : 1 + Number(+id > 3);
}

export const getStudent = (id: number): Student => {
    return students.filter(stud => stud.id === id)[0];
}

export const getStudents = (): Array<Student> => {
    return students;
}