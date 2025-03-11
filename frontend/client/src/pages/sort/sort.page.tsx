/* Lib imports */
import { useState, useEffect } from "react";
import { useParams } from "react-router";
import { DndContext, DragEndEvent } from '@dnd-kit/core';

/* Types */
import { StudentWithLocation } from "../../types/Student";
import { ColumnCreation, ColumnType } from "../../types/Columns";

/* Components, services & etc. */
import SortColumn from "../../components/sort-column/sort-column.component";
import { markStudentAsApplied, updateStudentsLabels } from "./label-updater";
import { addStudentsLocations } from "./students-to-columns";
import { useAuth } from "../../services/auth/auth.provider";
import { getStudents } from "../../services/student/student.service";
import { handleDragEnd } from "./drag-helpers";
import { sortFunc } from "./sorting";

/* Styling */
import "./sort.page.scss";


const Sort = () => {
    let { id } = useParams();
    const { token } = useAuth();

    const [ students, setStudents ] = useState<Array<StudentWithLocation>>([]);
    const [ isDragging, setDragging ] = useState<boolean>(false);

    useEffect(() => {
        const gotStudents = getStudents(+id!, token!);
        gotStudents.then(addStudentsLocations(ColumnCreation.Initial))
                   .then(setStudents);
        
        // Mark all students as applied to this project
        gotStudents.then(all => all.forEach(student => markStudentAsApplied(id!, student.id)));
        // Should use a lifecycle hook but can't be bothered atm :=)
    }, []);

    
    const onDragEnd = (event: DragEndEvent) => {
        setDragging(false);
        updateStudentsLabels(id!, event);
        handleDragEnd(students, setStudents)(event);
    }

    const handleTeamBuild = () => {
        setStudents(
            addStudentsLocations(ColumnCreation.Request)(students.map(wrapped => wrapped.student))
        );
    }

    return (
        <div className="container">
            <div className="head">
                <h1>Sorting { id }</h1>
                <button className="build-team" onClick={handleTeamBuild}>Build team</button>
            </div>
            <div className="columns">
                <DndContext onDragEnd={onDragEnd} onDragStart={() => setDragging(true)}>
                    {
                        Object.keys(ColumnType)
                            .filter(v => isNaN(Number(v)))
                            .map((col, idx) => 
                                <SortColumn
                                    key={idx}
                                    id={idx}
                                    name={col}
                                    sorter={sortFunc("default")}
                                    isDragging={isDragging}
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
        </div>
    );
}

export default Sort;