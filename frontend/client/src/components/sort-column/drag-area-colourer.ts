/* Types */
import { DragAreaStyle } from "../../types/Dragging"


export const colourer = (isDragging: boolean): DragAreaStyle => {
    return isDragging ?
        {
            "background-color": "rgb(62 159 238 / 42%)",
            "border": "dashed 1px blue",
        } : {}
}