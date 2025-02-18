import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { DndContext } from '@dnd-kit/core';

import { getStudents, getStudentStatus } from "../../services/student/student.service";

import SortColumn from "../../components/sort-column/sort-column.component";

import "./sort.page.scss";

const COLUMNS = [
    "All", "Potential", "Selected"
];

const Sort = () => {
    const [ students, setStudents ] = useState(getStudents)

    useEffect(() => {
        setStudents(
            students.map((student) => { return {...student, column: getStudentStatus(student.id)}})
        )
    }, [])

    let { id } = useParams();
    
    function handleDragEnd(event) {
        const { active, over } = event;
    
        if (!over) return;
    
        const taskId = active.id;
        const newColumn = over.id;
    
        setStudents(() =>
            students.map((student) =>
                student.id === taskId
              ? {
                  ...student,
                  column: newColumn,
                }
              : student,
          ),
        );
      }

    return (
        <>
            <h1>Sorting { id }</h1>

            <div id="columns">
                <DndContext onDragEnd={handleDragEnd}>
                    {
                        COLUMNS.map((col, idx) => 
                            <SortColumn key={idx} id={idx} name={col} items={students.filter((student) => student.column === idx)} />
                        )
                    }
                </DndContext>
            </div>
        </>
    );
}

export default Sort;