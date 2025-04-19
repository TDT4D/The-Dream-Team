/* Components, services & etc. */
import { useState } from "react";
import { useAuth } from "../../services/auth/auth.provider";
import { initML } from "../../services/score/score.service";
import { isML_up, setML_status } from "../../services/ML/ml.service";

/* Styling */
import "./training.page.scss";

type TrainingStatus = "uninitialized" | "error" | "initialized" | "loading";

const Training = () => {
    const { token } = useAuth();
    const [ trainStatus, setTrainStatus ] = useState<TrainingStatus>(() => isML_up() ? "initialized" : "uninitialized");
    
    const statusToMsg = (status: TrainingStatus) => {
        switch (status) {
            case "error":
                return <p>There was an error!</p>
            case "uninitialized":
                return <></>;
            case "initialized":
                return <p>Succesfully initialized ML model!</p>
            case "loading":
                return <p>Training the ML model. This may take a second...</p>
            default:
                break;
        }
    }

    return <div className="training-page">
        {
            token ?
            <>
                <div className="initializer">
                    <h2>Initialize the ML model:</h2>
                    <button onClick={() => {
                        setTrainStatus("loading");
                        const req = initML(token!);
                        req.then(setML_status);
                        req.then(() => setTrainStatus("initialized"));
                    }}>Initialize</button>
                </div>
                <span className="training-status">
                    { statusToMsg(trainStatus) }
                </span>
            </>
            :
            <p>Please log in!</p>
        }
    </div>
}

export default Training;