export type Score = {
  score: number;
  motivation: number;
};

export type ScoreRequest = {
  studentId: number;
  Score: number;
  motivation: number;
};

export type ProjectScore = {
  projectId: number;
  scores: ScoreRequest[];
};

export type ProjectTeam = {
  projectId: number;
  team: ScoreRequest[];
};

export type TeamMember = {
  studentId: number;
};

export type NewStudentScore = {
  projectId: number;
  studentId: number;
  whyProject: number;
  whyExperience: number;
  location_match: number;
  field: number;
  score: number;
  motivation_score: number;
  final_score: number;
};

export type ProjectDreamTeam = {
  best_overall: NewStudentScore[];
  perfect_team: NewStudentScore[];
  diverse_teams: NewStudentScore[][];
};
