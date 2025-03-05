export type Project = {
    id: number,
    name: string,
    description: string,
    batchesIds: number[],
    tags: string[],
    themes: string[],
}

export const defaultProjects: Project[] = [
    {
        id: 1,
        name: "test 1",
        description: "bla bla",
        batchesIds: [1],
        tags: ["best", "tags"],
        themes: ["bestest", "theme"],
    },
    {
        id: 2,
        name: "test 2",
        description: "bla bla",
        batchesIds: [1],
        tags: ["best", "tags"],
        themes: ["bestest", "theme"],
    },
    {
        id: 3,
        name: "test 3",
        description: "bla bla",
        batchesIds: [1],
        tags: ["best", "tags"],
        themes: ["bestest", "theme"],
    },
];