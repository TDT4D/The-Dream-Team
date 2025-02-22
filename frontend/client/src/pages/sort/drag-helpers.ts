/* Lib imports */
import { DragEndEvent } from "@dnd-kit/core";

/* Types */
import { DragID } from "../../types/Dragging";
import { StudentWithLocation } from "../../types/Student";

// NOTE: This is basically dark magic and I don't wanna explain this ever. But this should work :)

export const handleDragEnd = (students: StudentWithLocation[], setStudents: Function) => {
    return (event: DragEndEvent) => {
        const { active, over } = event;

        if (!over) return;
        
        const dragging = JSON.parse(active.id as string) as DragID;
        const target = JSON.parse(over.id as string) as DragID;

        const card = students.filter((student) => student.student.id === dragging.cardId!)[0];

        setStudents(
            () => students
                .map(createNewStudentWithLoc(dragging, target, card.row))
                .map(handleOtherRowUpdates(dragging, target, card.row))
        );
    }
}

const handleOtherRowUpdates = (dragging: DragID, target: DragID, old_row: number) => {
    return (current: StudentWithLocation, _: number, arr: StudentWithLocation[]): StudentWithLocation => {
        const newRow = arr.filter(w => w.student.id === dragging.cardId)[0].row;

        // Update all the cards that need to move up (dec. row)
        if ( current.column === dragging.columnId &&
            current.student.id != dragging.cardId! &&
            current.row > old_row &&
            (dragging.columnId != target.columnId || current.row <= newRow)) {
            return { ...current, row: current.row - 1 };
        }
        
        // Update all the cards that need to move down (inc. row)
        if ( target.cardId != undefined &&
            current.column === target.columnId &&
            current.student.id != dragging.cardId! &&
            current.row >= newRow &&
            (dragging.columnId != target.columnId || current.row <= old_row) ) {
            return { ...current, row: current.row + 1 };
        }
        // Yeah... I hate this too...
        return current;
    }
}

const createNewStudentWithLoc = (dragging: DragID, target: DragID, old_row: number) => {
    return (current: StudentWithLocation, _: number, arr: StudentWithLocation[]): StudentWithLocation => {
        // Case: Not the card we are moving
        if (current.student.id != dragging.cardId!) return { ...current };
        
        // Case: We are moving to a column
        if (target.cardId === undefined) {
            const row = arr.filter(w => w.column === target.columnId).length;
            return { student: current.student, column: target.columnId, row }
        }
        // Case: We are moving on to a card in a different column
        const targetRow = arr.filter(w => w.student.id === target.cardId)[0].row;
        const row = targetRow + Number(dragging.columnId != target.columnId || targetRow < old_row);
        return { student: current.student, column: target.columnId, row }
    }
}
