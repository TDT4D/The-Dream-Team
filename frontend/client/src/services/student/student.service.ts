/* Types */
import { AuthToken } from "../../types/Auth";
import { Project } from "../../types/Project";
import { Student } from "../../types/Student";

/* Components, services & etc. */
import { callAPI, USE_SERVER } from "../api/api.service";
import { defaultStudentsForEachProject } from "./default-students";

export const getStudents = (
  projectID: Project["id"],
  token: AuthToken,
): Promise<Student[]> => {
  const errorHandler = (reason: any): Student[] => {
    console.log("[GET STUDENTS ERROR] --- " + reason);
    return [];
  };

    return USE_SERVER ? callAPI<Student[]>(`/projects/${projectID}/students`, token).catch(errorHandler) : Promise.resolve(defaultStudentsForEachProject(projectID));
}
