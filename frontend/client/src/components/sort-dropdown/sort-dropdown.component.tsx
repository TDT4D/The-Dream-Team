/* Lib imports */
import { Popover, PopoverContent, PopoverTrigger } from "@heroui/popover";

/* Types */
import { SortMethod } from "../../types/SortMethods";

/* Styling */
import "./sort-dropdown.component.scss";
import dropdownIcon from "./dropdown-icon.svg";
import { useState } from "react";

type SortDropdownProps = {
    setSortType: React.Dispatch<React.SetStateAction<SortMethod>>,
    setAscending: React.Dispatch<React.SetStateAction<boolean>>
}

type MethodButtonType = {
    method: SortMethod,
    ascending?: boolean
}

const SortDropdown = ({ setSortType, setAscending}: SortDropdownProps) => {
    const [ activeMethod, setActiveMethod ] = useState<MethodButtonType>({ method: "default"});

    const createMethodButton = (method: SortMethod, ascending?: boolean) => <>
    <button className="method" disabled={method === activeMethod.method && ascending === activeMethod.ascending} onClick={() => {
        setSortType(method);
        setActiveMethod({ method, ascending });
        if (ascending !== undefined) setAscending(ascending);
    }}>
        {ascending !== undefined && method[0].toUpperCase() + method.substring(1).toLowerCase()} {ascending ? "ascending" : ascending === undefined ? "None" : "descending"}
    </button>
</>


    return <div className="sort-dropdown">
        <Popover placement="bottom" shouldCloseOnBlur={true}>
            <PopoverTrigger>
                <button className="drop">
                    Select sort method
                    <img className="icon" src={dropdownIcon}/>
                </button>
            </PopoverTrigger>
            <PopoverContent>
                <div className="method-dropdown">
                    { createMethodButton("default") }
                    { createMethodButton("name", true) }
                    { createMethodButton("name", false) }
                    { createMethodButton("score", true) }
                    { createMethodButton("score", false) }
                    { createMethodButton("motivation", true) }
                    { createMethodButton("motivation", false) }
                </div>
            </PopoverContent>
        </Popover>
    </div>
}

export default SortDropdown;