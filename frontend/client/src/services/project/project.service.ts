/* Types */
import { AuthToken } from "../../types/Auth";
import { Project } from "../../types/Project";

/* Components, services & etc. */
import { callAPI, USE_SERVER } from "../api/api.service";
import { defaultProjects } from "./default-projects";

export const getProjects = async (token: AuthToken): Promise<Project[]> => {
    
    const errorHandler = (reason: any): Project[] => {
        console.log("[GET PROJECTS ERROR] --- " + reason);
        return [];
    }

    return USE_SERVER ? callAPI<Project[]>("/projects", token).catch(errorHandler) : Promise.resolve(defaultProjects);
}
