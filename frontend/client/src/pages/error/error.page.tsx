type ErrorProps = {
    reason?: string
}

const Error = ({ reason }: ErrorProps) => {
    return (
        <>
            <h1>Error</h1>
            <span>
                { reason? reason : "An error occoured!" }
            </span>
        </>
    );
}

export default Error;