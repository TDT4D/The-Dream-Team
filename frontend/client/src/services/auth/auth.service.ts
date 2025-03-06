/* Types */
import { AuthToken } from "../../types/Auth";

// Has to get token from local storage
export const getAuthToken = (): AuthToken => {
    return {
        Authorization: "Bearer bla-bla-bla",
    }
}