import { useDroppable } from "@dnd-kit/core";

import StudentCard from "../student-card/student-card.component";
import { Student } from "../../types/Student";

import "./sort-column.component.scss";


type SortColumnProps = {
    id: number,
    name: string,
    students: Array<Student>
}

const SortColumn = ({ id, name, students }: SortColumnProps) => {
    const { setNodeRef } = useDroppable({
        id
    });

    return (
        <div className="column">
            <span> { name } </span>
            <div ref={setNodeRef} className="drag-area">
                {
                    students.map((student, idx) => <StudentCard key={idx} student={student} />)
                }
            </div>
        </div>
    );
}

export default SortColumn;