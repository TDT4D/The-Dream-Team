/* Types */
import { Project } from "../../types/Project";
import { ProjectScore } from "../../types/Score";

/* Components, services & etc. */
import {
  defaultStudentsForEachProject,
  hashCode,
} from "../student/default-students";

export const defaultScoreFetcher = (projectId: Project["id"]): ProjectScore => {
  return {
    projectId,
    scores: defaultStudentsForEachProject(projectId).map((student) => {
      const hash = hashCode(JSON.stringify(student));
      return {
        studentId: student.id,
        Score: ((0x0000ffff & hash) / 0x0000ffff) * 100,
        motivation: (((0xffff0000 & hash) >> 16) / 0x7fff) * 100,
      };
    }),
  };
};
