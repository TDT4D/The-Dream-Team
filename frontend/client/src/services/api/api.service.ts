import { getAuthToken } from "../auth/auth.service";

const API_ENDPOINT = import.meta.env.API_ENDPOINT || "/api";

type HTTP_Methods = "GET" | "POST";

export async function callAPI<T>(path: string, method: HTTP_Methods = "GET"): Promise<T> {
    const response = await fetch(
        `${API_ENDPOINT}${path}`,
        {
            method,
            headers: {
                ...getAuthToken()
            }
        }
    );
    
    if (!response.ok) {
      throw new Error(response.statusText);
    }

    return await response.json() as T;
}

export const USE_SERVER: boolean = !(import.meta.env.MODE === "development");
