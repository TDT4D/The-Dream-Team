import { getStudent } from "../../services/student/student.service";
import { useDraggable } from "@dnd-kit/core";

import Label from "../label/label.component";

import "./student-card.component.scss";

const StudentCard = ({ student }) => {    
    const { attributes, listeners, setNodeRef, transform } = useDraggable({
        id: student.id,
    });
    
    const style = transform
    ? {
        transform: `translate(${transform.x}px, ${transform.y}px)`,
        }
    : undefined;
    
    return (
        <div className="student-card"
        ref={setNodeRef}
        {...listeners}
        {...attributes}
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