import { useState, useEffect } from "react";
import { useParams } from "react-router";
import { DndContext, DragEndEvent } from '@dnd-kit/core';

import { getStudents, getStudentStatus } from "../../services/student/student.service";
import SortColumn from "../../components/sort-column/sort-column.component";
import { Student } from "../../types/Student";

import "./sort.page.scss";

const COLUMNS = [
    "All", "Potential", "Selected"
];

type StudentWithCol = {
    student: Student,
    column?: number
}

const wrapStudent = (student: Student): StudentWithCol => {
    return { student }
}

const Sort = () => {
    const [ students, setStudents ] = useState<Array<StudentWithCol>>(getStudents().map(wrapStudent))

    useEffect(() => {
        setStudents(
            students.map((wrapped) => { return { student: wrapped.student, column: getStudentStatus(wrapped.student.id)}})
        )
    }, [])

    let { id } = useParams();
    
    function handleDragEnd(event: DragEndEvent) {
        const { active, over } = event;
    
        if (!over) return;
    
        const taskId = active.id as number;
        const newColumn = over.id as number;

        setStudents(
            () => students.map(
                (wrapped) => wrapped.student.id === taskId ? { ...wrapped, column: newColumn } : wrapped
            )
        );
      }

    return (
        <>
            <h1>Sorting { id }</h1>

            <div id="columns">
                <DndContext onDragEnd={handleDragEnd}>
                    {
                        COLUMNS.map((col, idx) => 
                            <SortColumn key={idx} id={idx} name={col}
                                students={
                                    students
                                        .filter((wrapped) => wrapped.column != null ? +wrapped.column === idx : 0)
                                        .map((wrapped) => wrapped.student)
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