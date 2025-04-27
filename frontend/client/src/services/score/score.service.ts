/* Types */
import { AuthToken } from "../../types/Auth";
import { ML_initType } from "../../types/ML";
import { Project } from "../../types/Project";
import {
  ProjectDreamTeam,
  ProjectScore,
  ProjectTeam,
  TeamMember,
} from "../../types/Score";

/* Components, services & etc. */
import { callAPI, callAPI_raw, USE_SERVER } from "../api/api.service";
import { defaultScoreFetcher } from "./default-scores";

export const initML = (
  token: AuthToken,
  type: ML_initType,
): Promise<boolean> => {
  const errorHandler = (reason: any): boolean => {
    console.log("[ML INIT ERROR] --- " + reason);
    return false;
  };

  if (!USE_SERVER)
    return new Promise((res) => {
      setTimeout(() => res(true), type === "basic" ? 1_000 : 5_000);
    });

  return type === "basic"
    ? callAPI_raw(`/init`, token, "POST")
        .then((resp) => resp.ok)
        .catch(errorHandler)
    : callAPI_raw(`/initWithMotivation`, token, "POST")
        .then((resp) => resp.ok)
        .catch(errorHandler);
};

export const getScores = (
  projectID: Project["id"],
  token: AuthToken,
): Promise<ProjectScore> => {
  const errorHandler = (reason: any): ProjectScore => {
    console.log("[GET SCORES ERROR] --- " + reason);
    return { projectId: -1, scores: [] };
  };

  if (!USE_SERVER) return Promise.resolve(defaultScoreFetcher(projectID));

  // FIXME: REMOVE THAT DUMB env var check and handle that somehow else
  // return callAPI<ProjectScore>(`/projects/${projectID}/scores${import.meta.env.VITE_ML_TYPE === "advanced" ? "?scoreFile=score_default" : ""}`, token).catch(errorHandler);
  return callAPI<ProjectScore>(`/projects/${projectID}/scores`, token).catch(
    errorHandler,
  );
};

export const getTeam = (
  projectID: Project["id"],
  token: AuthToken,
  mlType: ML_initType,
  teamSize?: number,
): Promise<TeamMember[]> => {
  const errorHandler = (reason: any): TeamMember[] => {
    console.log("[GET SCORES ERROR] --- " + reason);
    return [];
  };

  if (!USE_SERVER) return Promise.reject("NO DEFAULT TEAM");

  if (mlType === "basic") {
    return callAPI<ProjectTeam>(`/projects/${projectID}/team`, token, "POST")
      .then((proj) =>
        proj.team.map((scoreReq) => ({ studentId: scoreReq.studentId })),
      )
      .catch(errorHandler);
  }

  return callAPI<ProjectDreamTeam>(
    `/projects/${projectID}/dream-team?applicants=clean_default&scores=score_default&motivations=motivation_score&team_size=${teamSize!}&save_file=dreamteam`,
    token,
    "POST",
  )
    .then((dreamTeam) =>
      dreamTeam.best_overall.map((teamMember) => ({
        studentId: teamMember.studentId,
        score: teamMember.score,
        motivation_score: teamMember.motivation_score,
      })),
    )
    .catch(errorHandler);
};
