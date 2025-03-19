/* Lib imports */
import { useDraggable, useDroppable } from "@dnd-kit/core";
import { Card, CardBody, CardHeader } from "@heroui/card";
import { Divider } from "@heroui/divider";

/* Types */
import { LabelType } from "../../types/Label";
import { DragID } from "../../types/Dragging";
import { Student } from "../../types/Student";

/* Components, services & etc. */
import { getStudentLabels } from "../../services/student/student.service";
import LabelComponent from "../label/label.component";
import Score from "../score/score.component";

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
        <Card
            isBlurred
            className="student-card"
            ref={refs}
            {...draggable.listeners}
            {...draggable.attributes}
            style={style}>
        <CardHeader className="card-header">
            <span>
                { student.name }
            </span>
            <Score studentID={student.id}/>
        </CardHeader>
        <Divider />
        <CardBody className="card-body">
            <span>Applied:</span>
            <div className="labels" id="applied">
                {
                    getStudentLabels(student.id, LabelType.Applied).map((labl, idx) => {
                        return <LabelComponent key={idx} name={labl.content} colour={"green"} />
                    })
                }
            </div>
            <span>Selected:</span>
            <div className="labels" id="selected">
                {
                    getStudentLabels(student.id, LabelType.Selected).map((labl, idx) => {
                        return <LabelComponent key={idx} name={labl.content} colour={"yellow"} />
                    })
                }
            </div>
        </CardBody>
        </Card>
    );
}

export default StudentCard;