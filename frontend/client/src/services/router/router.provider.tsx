/* Lib imports */
import { Navigate, Outlet, RouteObject, RouterProvider, createBrowserRouter } from "react-router";

/* Components, services & etc. */
import { useAuth } from "../auth/auth.provider";

import Base from "../../pages/base/base.page";
import Sort from "../../pages/sort/sort.page";
import Select from '../../pages/select/select.page';
import Error from "../../pages/error/error.page";


const publicRoutes: RouteObject[] = [
    {
        index: true,
        element: <Select />,
    },
    {
        path: "/sort",
        element: <Error reason={"sort without ID!"} />,
    },
    {
        path: "*",
        element: <Error reason={"Check path!"} />,
    },
];

export const Routes = () => {
    const { isLoggedIn } = useAuth();
    
    const protectedRoutes: RouteObject[] = [
        {
            path: "/",
            element: isLoggedIn ? <Outlet /> : <Navigate to="/login" />,
            children: [
                {
                    path: "/sort/:id",
                    element: <Sort />,
                },
            ],
        },
    ];
    
    const loginRoute: RouteObject = {
        path: "/login",
        element: isLoggedIn ? <Navigate to="/"/> : <Error reason={"Login not implemented!"} />,
    }
    
    const router = createBrowserRouter([{
        path: "/",
        element: <Base/>,
        children: [ ...publicRoutes, ...protectedRoutes, loginRoute ],
    }]);

    return <RouterProvider router={router} />;
};