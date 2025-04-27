/* Types */
import {
  Student,
  StudentWithColumn,
  StudentWithLocation,
} from "../../types/Student";
import { Project } from "../../types/Project";
import { AuthToken } from "../../types/Auth";
import { MLContextType } from "../../types/ML";

/* Components, services & etc. */
import { getStudentLocation } from "../../services/student/location.service";
import { getTeam } from "../../services/score/score.service";
import { ColumnType } from "../../types/Columns";

const createRowAdder = () => {
  const numPerCol: Array<number> = [0, 0, 0];
  return (studentW: StudentWithColumn): StudentWithLocation => {
    const row = numPerCol[studentW.column!];
    numPerCol[studentW.column!]++;
    return { ...studentW, row };
  };
};

export const addInitialStudentLocations = (
  projectId: Project["id"],
  students: Student[],
): StudentWithLocation[] => {
  return students
    .map((student) => {
      return { student, column: getStudentLocation(projectId, student.id) };
    })
    .map(createRowAdder());
};

export const addStudentLocationsViaML = async (
  projectId: Project["id"],
  students: Student[],
  token: AuthToken,
  mlContext: MLContextType,
): Promise<StudentWithLocation[]> => {
  if (!token) throw new Error("No token when getting project team!");

  const team = await getTeam(
    projectId,
    token,
    mlContext.ml_type,
    mlContext.teamSize,
  );
  const addLocation = (student: Student): ColumnType => {
    const val = team.filter((member) => member.studentId === student.id);
    return val.length > 0 ? ColumnType.Selected : ColumnType.Applied;
  };
  return students
    .map((student) => {
      return { student, column: addLocation(student) };
    })
    .map(createRowAdder());
};
