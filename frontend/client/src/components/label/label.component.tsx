/* Styling */
import "./label.component.scss";

type LabelProps = {
    name: string,
    colour: string
}

const Label = ({ name, colour }: LabelProps) => {
    
    return (
        <>
            <span className="label" style={{backgroundColor:  colour}}>
                { name }
            </span>  
        </>
    );
}

export default Label;