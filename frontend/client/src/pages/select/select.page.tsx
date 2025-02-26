/* Types */
import { Project } from "../../types/Project";

/* Components, services & etc. */
import ProjectSelect from "../../components/project-select/project-select.component";

const testProjects: Array<Project> = [
    {
        id: 1,
        name: "test 1",
    },
    {
        id: 2,
        name: "test 2",
    },
    {
        id: 3,
        name: "test 3",
    }
];

const Select = () => {
    return (
        <ul>
            {
                testProjects.map((proj, index) => (
                    <li key={index}><ProjectSelect id={proj.id} name={proj.name}/></li>
                ))
            }
    </ul>
    )
}

export default Select;