/* Lib imports */
// import { Divider } from "@heroui/divider"

/* Types */
import { Student } from "../../types/Student"

/* Styling */
import "./score.component.scss";

type ScoreProps = {
    studentID: Student["id"]
}

const Score = ({studentID}: ScoreProps) => {
    // TODO: get score
    studentID += 1;
    
    return (
        <div className="score-label">
            <span className="score">{ studentID }</span>
            <span className="team">{ studentID < 3 ? 0 : 1}</span>
        </div>
    )
}

export default Score;