/* Types */
import { Project } from "../../types/Project";

const testProjects: Array<Project> = [
    {
        id: 1,
        name: "test 1",
    },
    {
        id: 2,
        name: "test 2",
    },
    {
        id: 3,
        name: "test 3",
    }
];

export const getProjects = (): Array<Project> => {
    return testProjects
}