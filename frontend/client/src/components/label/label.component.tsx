/* Styling */
import "./label.component.scss";

type LabelProps = {
    name: string,
    colour: string
}

const Label = ({ name }: LabelProps) => {
    
    return (
        <>
            <span className="label">
                { name }
            </span>  
        </>
    );
}

export default Label;