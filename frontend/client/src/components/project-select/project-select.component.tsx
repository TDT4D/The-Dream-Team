/* Lib imports */
import { useNavigate } from "react-router";

/* Types */
import { Project } from "../../types/Project";

/* Components, services & etc. */
import { useProjectContext } from "../../services/project/project.provider";

/* Styling */
import "./project-select.component.scss";

type ProjectSelectProps = {
    project: Project
}

const ProjectSelect = ({ project }: ProjectSelectProps) => {
    const { setAsCurrentProject } = useProjectContext();
    const navigate = useNavigate();
    
    const onClick = () => {
        setAsCurrentProject(project);
        navigate(`/sort/${project.id}`)
    }
    
    return (
        <div className="project-select-element">
            <button className="select-button" onClick={onClick}>
                { project.name }
            </button>
        </div>
    );
};

export default ProjectSelect;