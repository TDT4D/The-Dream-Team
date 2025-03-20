/* Lib imports */
import { DragEndEvent } from "@dnd-kit/core";

/* Types */
import { DragID } from "../../types/Dragging";
import { LabelType } from "../../types/Label";
import { Student } from "../../types/Student";

/* Components, services & etc. */
import { addLabelIfMissing, removeLabelFromStudent } from "../../services/student/student.service";

// Just a utility function atm
const columnIdToLabelType = (id: number): LabelType | undefined => {
    switch (id) {
        case 0: return LabelType.Applied;
        case 1: return undefined;
        case 2: return LabelType.Selected;
        default: throw new Error("Invalid column ID!");
    }
}

export const markStudentAsApplied = (projectName: string, studentId: Student["id"]): void => {
    addLabelIfMissing(studentId, { isType: LabelType.Applied, contains: { content: projectName }});
}

export const updateStudentsLabels = (projectName: string, event: DragEndEvent): void => {
    const { active, over } = event;
    
    if (!over) return;

    const card = JSON.parse(active.id as string) as DragID;
    const oldColumn = columnIdToLabelType(card.columnId);
    const newColumn = columnIdToLabelType((JSON.parse(over.id as string) as DragID).columnId);

    if (oldColumn === newColumn) return;
    if (oldColumn !== LabelType.Selected && newColumn !== LabelType.Selected) return;

    if (oldColumn === LabelType.Selected) {
        removeLabelFromStudent(card.cardId!, { isType: LabelType.Selected, contains: { content: projectName }});
        console.log()
        return;
    }
    addLabelIfMissing(card.cardId!, { isType: LabelType.Selected, contains: { content: projectName }});
}