import { useDroppable } from "@dnd-kit/core";
import StudentCard from "../student-card/student-card.component";

import "./sort-column.component.scss";
import { Student } from "../../services/student/student.service";

type SortColumnProps = {
    id: number,
    name: string,
    items: Array<Student>
}

const SortColumn = ({ id, name, items }: SortColumnProps) => {
    const { setNodeRef } = useDroppable({
        id
    });

    return (
        <div className="column">
            <span> { name } </span>
            <div ref={setNodeRef} className="drag-area">
                {
                    items.map((student, idx) => <StudentCard key={idx} student={student} />)
                }
            </div>
        </div>
    );
}

export default SortColumn;