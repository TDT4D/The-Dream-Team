/* Lib imports */
import { useEffect, useState } from "react";
import { Popover, PopoverContent, PopoverTrigger } from "@heroui/popover";

/* Types */
import { Project } from "../../types/Project";

/* Components, services & etc. */
import ProjectSelect from "../../components/project-select/project-select.component";
import { getProjects } from "../../services/project/project.service";

/* Styling */
import "./select.page.scss";

const Select = () => {
    const [ projects, setProjects ] = useState<Project[]>([]);

    useEffect(() => {
        getProjects().then(setProjects);
    }, []);

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
                                projects.map((proj, index) => (
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