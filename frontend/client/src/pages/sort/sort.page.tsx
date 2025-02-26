/* Lib imports */
import { useState, useEffect } from "react";
import { useParams } from "react-router";
import { DndContext } from '@dnd-kit/core';

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
    const [ students, setStudents ] = useState<Array<StudentWithLocation>>([]);

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

    let { id } = useParams();

    return (
        <>
            <h1>Sorting { id }</h1>

            <div id="columns">
                <DndContext onDragEnd={handleDragEnd(students, setStudents)}>
                    {
                        COLUMNS.map((col, idx) => 
                            <SortColumn key={idx} id={idx} name={col} sorter={sortFunc("default")}
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