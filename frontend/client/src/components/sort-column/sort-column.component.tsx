/* Lib imports */
import { useDroppable } from "@dnd-kit/core";

/* Types */
import { Student, StudentWithRow } from "../../types/Student";
import { StudentSorter } from "../../types/SortMethods";
import { DragID } from "../../types/Dragging";

/* Components, services & etc. */
import StudentCard from "../student-card/student-card.component";
import { colourer } from "./drag-area-colourer";

/* Styling */
import "./sort-column.component.scss";

type SortColumnProps = {
    id: number,
    name: string,
    students: Array<StudentWithRow>,
    sorter: StudentSorter,
    isDragging: boolean
}

const studentExtractor = (wrapped: StudentWithRow): Student => {
    return {...wrapped.student};
}

const SortColumn = ({ id, name, students, sorter, isDragging }: SortColumnProps) => {
    const dragId: DragID = { columnId: id };

    const { setNodeRef } = useDroppable({
        id: JSON.stringify(dragId)
    });

    return (
        <div className="column">
            <div className="column-name"> { name } </div>
            <div ref={setNodeRef} className="drag-area" style={colourer(isDragging)}>
                {
                    students
                        .sort(sorter)
                        .map((student, idx) => <StudentCard key={idx} student={studentExtractor(student)} columnId={id} />)
                }
            </div>
        </div>
    );
}

export default SortColumn;