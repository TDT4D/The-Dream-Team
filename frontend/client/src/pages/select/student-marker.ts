import { getStudents, removeAllLabelsByType } from "../../services/student/student.service";
import { AuthToken } from "../../types/Auth";
import { LabelType } from "../../types/Label";
import { Project } from "../../types/Project";
import { Student } from "../../types/Student";
import { markStudentAsApplied } from "../sort/label-updater";


export default (token: AuthToken) => {
    return (projects: Project[]): Project[] => {

        // Pair all projects with the applied students
        const intermediary = projects.map(project => { return { project, students: getStudents(project.id, token) }});

        // Remove all "Applied" labels from all students (just in case)
        {
            // In an own scope to release the "students" variable
            const students: Set<Student> = new Set<Student>();
            intermediary.forEach(value => {
                value.students.then(_students => _students.forEach(student => students.add(student)))
            });
            students.forEach(student => removeAllLabelsByType(student.id, LabelType.Applied));
        }
        
        // Go through each project and mark all students that have applied as "Applied"
        intermediary.forEach(pairing => {
            pairing.students.then(students => students.forEach(student => markStudentAsApplied(pairing.project.name, student.id)));
        });

        return projects;
    }
}