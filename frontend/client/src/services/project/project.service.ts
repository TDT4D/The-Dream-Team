/* Types */
import { Project } from "../../types/Project";

/* Components, services & etc. */
import { callAPI, USE_SERVER } from "../api/api.service";

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

export const getProjects = async (): Promise<Project[]> => {
    return USE_SERVER ? callAPI<Project[]>("/projects") : Promise.resolve(testProjects);
}
