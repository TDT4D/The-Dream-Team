const students  = [
    {
        id: "0",
        name: "Student Test0",
        labels: [
            "x"
        ],
    },
    {
        id: "1",
        name: "Student Test1",
        labels: [
            "x", "y"
        ],
    },
    {
        id: "2",
        name: "Student Test2",
        labels: [
            "y"
        ],
    },
    {
        id: "3",
        name: "Student Test3",
        labels: [
            "x", "z"
        ],
    },
    {
        id: "4",
        name: "Student Test4",
        labels: [
            "x", "y", "z"
        ],
    },
]

type Student = {
    id: string,
    name: string
    labels: Array<String>
}

export type { Student };

export const getStudentStatus = (id: string): string => {
    return String(+id < 3 ? 0 : 1 + Number(+id > 3));
}

export const getStudent = (id: string): Student => {
    return students.filter(stud => stud.id === id)[0];
}

export const getStudents = (): Array<Student> => {
    return students;
}