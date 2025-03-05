/* Types */
import { Project } from "../../types/Project";

/* Components, services & etc. */
import { callAPI, USE_SERVER } from "../api/api.service";
import { defaultProjects } from "./default-projects";

export const getProjects = async (): Promise<Project[]> => {
    return USE_SERVER ? callAPI<Project[]>("/projects") : Promise.resolve(defaultProjects);
}
