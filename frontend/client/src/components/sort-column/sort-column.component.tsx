/* Lib imports */
import { useDroppable } from "@dnd-kit/core";

/* Types */
import { Student, StudentWithRow } from "../../types/Student";
import { StudentSorter } from "../../types/SortMethods";
import { DragID } from "../../types/Dragging";

/* Components, services & etc. */
import StudentCard from "../student-card/student-card.component";

/* Styling */
import "./sort-column.component.scss";

type SortColumnProps = {
    id: number,
    name: string,
    students: Array<StudentWithRow>,
    sorter: StudentSorter
}

const studentExtractor = (wrapped: StudentWithRow): Student => {
    return {...wrapped.student};
}

const SortColumn = ({ id, name, students, sorter }: SortColumnProps) => {
    const dragId: DragID = { columnId: id };

    const { setNodeRef } = useDroppable({
        id: JSON.stringify(dragId)
    });

    return (
        <div className="column">
            <span> { name } </span>
            <div ref={setNodeRef} className="drag-area">
                {
                    students.sort(sorter).map((student, idx) => <StudentCard key={idx} student={studentExtractor(student)} columnId={id} />)
                }
            </div>
        </div>
    );
}

export default SortColumn;