import { Link } from "react-router-dom";

const ProjectSelect = ({id, name}) => {
    return (
        <Link to={"/sort/" + id}>
            <span>{ id }</span>
            <span>{ name } </span>
        </Link>
    );
};

export default ProjectSelect;