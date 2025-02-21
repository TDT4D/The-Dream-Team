import React from "react";
import { Link } from "react-router-dom";

type ProjectSelectProps = {
    id: number,
    name: string
}

const ProjectSelect = ({id, name}: ProjectSelectProps) => {
    return (
        <Link to={"/sort/" + id}>
            <span>{ id }</span>
            <span>{ name } </span>
        </Link>
    );
};

export default ProjectSelect;