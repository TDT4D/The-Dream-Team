import { createContext, ReactNode, useContext, useMemo, useState } from "react";
import { Project } from "../../types/Project";

type ProjectProviderType = {
    currentProject?: Project,
    setAsCurrentProject: (project: Project) => void
}

type ProjectProviderProps = {
    children: ReactNode
}

const ProjectContext = createContext<ProjectProviderType>({setAsCurrentProject: () => {}});

export const ProjectProvider = ({ children }: ProjectProviderProps) => {
    const [ project, setProject ] = useState<Project>();

    const setAsCurrentProject = (project: Project) => {
        setProject(project);
    }

    const contextValue = useMemo(
        () => ({
            currentProject: project,
            setAsCurrentProject
        }),
        [ project ]
    )

    return <ProjectContext.Provider value={contextValue}>{children}</ProjectContext.Provider>
}

export const useProjectContext = () => {
    return useContext(ProjectContext);
}