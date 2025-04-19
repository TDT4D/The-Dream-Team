/* Types */
import { Score as ScoreType } from "../../types/Score";

/* Styling */
import "./score.component.scss";

type ScoreProps = {
    score?: ScoreType
}

const Score = ({ score }: ScoreProps) => {
    const dispScore = score? Math.round(score.score) : undefined;
    const dispMotivation = score? Math.round(score.motivation) : undefined;

    const hueMin = 25;
    const hueMax = 95;

    return (
        <div className="score-label">
            {
                score ?
                <>
                    <span className="score" style={{"backgroundColor": `hsl(${(hueMax-hueMin) * dispScore! / 100 + hueMin}, 95%, 50%)`}}>
                        { dispScore }%
                    </span>
                    <span className="motivation" style={{"backgroundColor": `hsl(360, 0%, ${25 * dispMotivation! / 100 + 75}%)`}}>
                        { dispMotivation }%
                    </span>
                </>
                : <span className="loading">Loading Score...</span>
            }
        </div>
    )
}

export default Score;