/* Lib imports */
import { useDraggable, useDroppable } from "@dnd-kit/core";

/* Types */
import { DragID } from "../../types/Dragging";
import { Student } from "../../types/Student";

/* Components, services & etc. */
import Label from "../label/label.component";

/* Styling */
import "./student-card.component.scss";

type StudentCardProps = {
    student: Student,
    columnId: number
}

const StudentCard = ({ student, columnId }: StudentCardProps) => {    
    const dragId: DragID = {
        columnId,
        cardId: student.id
    };
    
    const draggable = useDraggable({ id: JSON.stringify(dragId), });
    const droppable = useDroppable({ id: JSON.stringify(dragId), });

    const refs = (e: HTMLElement | null) => {
        draggable.setNodeRef(e);
        droppable.setNodeRef(e);
    }

    const style = draggable.transform ? { transform: `translate(${draggable.transform.x}px, ${draggable.transform.y}px)`, } : undefined;

    return (
        <div className="student-card"
        ref={refs}
        {...draggable.listeners}
        {...draggable.attributes}
        style={style}>
            <span>
                { student.name }
            </span>
            <div className="labels">
                { student.labels.map((labl, idx) => {
                    return <Label key={idx} name={labl} colour={"green"} />
                }) }
            </div>
        </div>
    );
}

export default StudentCard;