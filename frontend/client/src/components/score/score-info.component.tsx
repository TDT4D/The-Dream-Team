import { Popover, PopoverContent, PopoverTrigger } from "@heroui/popover"

/* Styling */
import "./score-info.component.scss";
import infoIcon from "./info-icon.svg";
import scoreInfo from "./score.svg";


const ScoreInfo = () => {
    return <>
        <Popover placement="bottom">
            <PopoverTrigger>
                <button className="info">
                    <img className="info-icon" src={infoIcon}/>
                </button>
            </PopoverTrigger>
            <PopoverContent>
                <div className="score-info">
                    <h4>Information about the scores</h4>
                    <div>The percentages on the applicant card are the skill score</div>
                    <div>and the motivation score.</div>
                    <div>The maximum of both scores is 100%</div>
                    <img className = "score-example" src={scoreInfo}/>
                </div>
            </PopoverContent>
        </Popover>
    </>
}

export default ScoreInfo;