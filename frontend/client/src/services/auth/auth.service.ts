/* Types */
import { AuthToken } from "../../types/Auth";

export const getAuthToken = (): AuthToken => {
    return {
        Authorization: "Bearer bla-bla-bla",
    }
}