/* Lib imports */
import { Link } from "react-router";

/* Styling */
import "./project-select.component.scss";

type ProjectSelectProps = {
    id: number,
    name: string
}

const ProjectSelect = ({id, name}: ProjectSelectProps) => {
    return (
        <div className="project-select-element">
            <Link className="link" to={`/sort/${id}`}>
                <span>{ name } </span>
            </Link>
        </div>
    );
};

export default ProjectSelect;