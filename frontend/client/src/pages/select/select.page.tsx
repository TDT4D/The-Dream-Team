/* Lib imports */
import { Popover, PopoverContent, PopoverTrigger } from "@heroui/popover";

/* Components, services & etc. */
import ProjectSelect from "../../components/project-select/project-select.component";
import { getProjects } from "../../services/project/project.service";

/* Styling */
import "./select.page.scss";

const Select = () => {
    return (
        <div className="select">
            <h1>
                The Dream Team
            </h1>
            <div className="project-select">
                <Popover placement="bottom">
                    <PopoverTrigger>
                        <button className="drop">
                            <span>Select project</span>
                            <span className="icon">V</span>
                        </button>
                    </PopoverTrigger>
                    <PopoverContent>
                        <div className="dropdown">
                            {
                                getProjects().map((proj, index) => (
                                    <ProjectSelect key={index} id={proj.id} name={proj.name}/>
                                ))
                            }
                        </div>
                    </PopoverContent>
                </Popover>
            </div>
        </div>
    )
}

export default Select;