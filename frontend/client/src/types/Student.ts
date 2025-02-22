export type Student = {
    id: number,
    name: string
    labels: Array<string>
}

export type StudentWithColumn = {
    student: Student,
    column: number
}

export type StudentWithRow = {
    student: Student,
    row: number
}

export type StudentWithLocation = {
    student: Student,
    column: number,
    row: number
}