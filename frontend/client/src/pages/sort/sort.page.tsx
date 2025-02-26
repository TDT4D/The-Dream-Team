/* Lib imports */
import { useState, useEffect } from "react";
import { useParams } from "react-router";
import { DndContext, DragEndEvent } from '@dnd-kit/core';

/* Types */
import { Student, StudentWithColumn, StudentWithLocation } from "../../types/Student";

/* Components, services & etc. */
import { getStudents, getStudentStatus } from "../../services/student/student.service";
import SortColumn from "../../components/sort-column/sort-column.component";
import { handleDragEnd } from "./drag-helpers";
import { sortFunc } from "./sorting";

/* Styling */
import "./sort.page.scss";

const COLUMNS = [
    "Applied", "Potential", "Selected"
];


const Sort = () => {
    let { id } = useParams();
    
    const [ students, setStudents ] = useState<Array<StudentWithLocation>>([]);
    const [ isDragging, setDragging ] = useState<boolean>(false);

    useEffect(() => {
        const addCol = (student: Student): StudentWithColumn => { return { student, column: getStudentStatus(student.id) }};
        
        const numPerCol: Array<number> = [0, 0, 0];
        const addRow = (studentW: StudentWithColumn): StudentWithLocation => {
            const row = numPerCol[studentW.column!];
            numPerCol[studentW.column!]++;
            return { ...studentW, row };
        }

        setStudents(
            getStudents().map(addCol).map(addRow)
        )
    }, [])

    
    const onDragEnd = (event: DragEndEvent) => {
        setDragging(false);
        handleDragEnd(students, setStudents)(event);
    }

    return (
        <>
            <h1>Sorting { id }</h1>

            <div id="columns">
                <DndContext onDragEnd={onDragEnd} onDragStart={() => setDragging(true)}>
                    {
                        COLUMNS.map((col, idx) => 
                            <SortColumn key={idx} id={idx} name={col} sorter={sortFunc("default")} isDragging={isDragging}
                                students={
                                    students
                                        .filter((wrapped) => wrapped.column != null ? +wrapped.column === idx : 0)
                                        .map(wrapped => { return { student: wrapped.student, row: wrapped.row }})
                                }
                            />
                        )
                    }
                </DndContext>
            </div>
        </>
    );
}

export default Sort;