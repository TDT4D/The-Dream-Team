import { AuthToken } from "../../types/Auth";

const API_ENDPOINT = import.meta.env.API_ENDPOINT || "/api";

type HTTP_Methods = "GET" | "POST";

export async function callAPI<T>(path: string, token: AuthToken, method: HTTP_Methods = "GET"): Promise<T> {
    const response = await fetch(
        `${API_ENDPOINT}${path}`,
        {
            method,
            headers: {
                ...token
            }
        }
    );
    
    if (!response.ok) {
        return Promise.reject("[API CALL !OK] -- " + response.statusText);
    }

    return await response.json() as T;
}

export const USE_SERVER: boolean = !(import.meta.env.MODE === "development");
