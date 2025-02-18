import "./label.component.scss";

const Label = ({ name, colour }) => {
    
    return (
        <>
            <span className="label" style={{backgroundColor:  colour}}>
                { name }
            </span>  
        </>
    );
}

export default Label;