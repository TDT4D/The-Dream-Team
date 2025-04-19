/* Lib imports */
import { useState, useEffect } from "react";
import { useParams } from "react-router";
import { DndContext, DragEndEvent } from '@dnd-kit/core';

/* Types */
import { StudentWithLocation } from "../../types/Student";
import { SortMethod } from "../../types/SortMethods";
import { ColumnType } from "../../types/Columns";

/* Components, services & etc. */
import SortColumn from "../../components/sort-column/sort-column.component";
import SortDropdown from "../../components/sort-dropdown/sort-dropdown.component";
import { updateAllStudentLabels, updateMovedStudentsLabels } from "./label-helpers";
import { setStudentLocationTo } from "../../services/student/location.service";
import { useProjectContext } from "../../services/project/project.provider";
import { addInitialStudentLocations, addStudentLocationsViaML } from "./students-to-columns";
import { useAuth } from "../../services/auth/auth.provider";
import { getStudents } from "../../services/student/student.service";
import { handleDragEnd, parseDragIDs } from "./drag-helpers";
import { addScoreForStudents } from "./score-helpers";
import { createStudentSorter } from "./sorting";

/* Styling */
import "./sort.page.scss";
import ScoreInfo from "../../components/score/score-info.component";


const Sort = () => {
    let { id } = useParams();
    const { token } = useAuth();
    const { currentProject } = useProjectContext();

    const [ students, setStudents ] = useState<Array<StudentWithLocation>>([]);
    const [ isDragging, setDragging ] = useState<boolean>(false);

    const [ sortType, setSortType ] = useState<SortMethod>("default");
    const [ isAscending, setAscending ] = useState<boolean>(true);

    useEffect(() => {
        if (token === undefined) return;

        const projectId = +id!;
        getStudents(projectId, token)
            .then(gotStudents => addInitialStudentLocations(projectId, gotStudents))
            .then(addScoreForStudents(projectId, token, setStudents));
    }, []);

    const onDragEnd = (event: DragEndEvent) => {
        setDragging(false);

        const projectId = +id!;
        const { dragging, target } = parseDragIDs(event)
        if (!target) return;

        // Update labels, student location and set the UI to match data
        updateMovedStudentsLabels(currentProject!.name, dragging, target);
        setStudentLocationTo(target.columnId, projectId, dragging.cardId!);
        handleDragEnd(students, setStudents)(dragging, target);
    }

    const handleTeamBuild = async () => {
        const projectId = +id!;
        const oldUnwrappedStudents = students.map(wrapped => wrapped.student);

        const newStudents = await addStudentLocationsViaML(projectId, oldUnwrappedStudents, token!);
        setStudents(newStudents);

        updateAllStudentLabels(currentProject!.name, newStudents);
        newStudents.forEach(wrappedStudent => setStudentLocationTo(wrappedStudent.column, projectId, wrappedStudent.student.id));
    }

    return (
        <div className="container">
            <div className="head">
                <h1>{ currentProject?.name }</h1>
                <ScoreInfo/>
                <SortDropdown setSortType={setSortType} setAscending={setAscending}/>
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
                                    sorter={createStudentSorter(sortType, !isAscending)}
                                    isDragging={isDragging}
                                    students={
                                        students
                                            .filter((wrapped) => +wrapped.column === idx)
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