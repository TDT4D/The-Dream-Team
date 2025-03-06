export type Student = {
    id: number,
    name: string,
    homeUniversity: string,
    attendingUniversity: string,
    city: string,
    cvLink: string,
    degreeLevelType: string,
    notes: string[],
    socialNetworkLinks: Map<string, string>,
    studiesDescription: string,
    studiesField: string,
    studiesType: string,
    whyGoodCreator: string,
    whyJoinDemola: string,
    whyRole: string,
    applications: ApplicationData[],
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

export type ApplicationData = {
    projectId: number,
    projectName: string,
    studentId: number,
    chosenBatch: number,
    relation: string,
    staffInsertion: boolean,
    dropoutExplanation: string,
    whyExperience: string,
    whyProject: string,
}