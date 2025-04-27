import { getScores } from "../../services/score/score.service";
import { AuthToken } from "../../types/Auth";
import { Project } from "../../types/Project";
import { ProjectScore } from "../../types/Score";
import { StudentWithLocation } from "../../types/Student";

export const addScoreForStudents = (
  projectId: Project["id"],
  token: AuthToken,
  setStudents: Function,
) => {
  return (students: StudentWithLocation[]): void => {
    // While we get scores
    setStudents(students);

    const update = (projectScores: ProjectScore) => {
      const out: StudentWithLocation[] = [];
      students.forEach((wrappedStudent) => {
        const { Score, motivation } = projectScores.scores.filter(
          (score) => score.studentId === wrappedStudent.student.id,
        )[0];
        out.push({
          ...wrappedStudent,
          student: {
            ...wrappedStudent.student,
            score: { score: Score, motivation }, // FIXME: Score to lowercase from ML side plz
          },
        });
      });
      return out;
    };

    getScores(projectId, token)
      .then(update)
      .then((v) => setStudents(v))
      .then(() => console.log("[GOT STUDENT SCORES]"));
  };
};
