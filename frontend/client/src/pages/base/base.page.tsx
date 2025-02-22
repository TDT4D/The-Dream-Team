/* Lib imports */
import { Outlet } from "react-router";

/* Components, services & etc. */
import Header from "../../components/header/header.component";

const APP_TITLE = "The Dream Team"

const Base = () => {
  return (
    <>
      <Header title={APP_TITLE}/>
      <Outlet />
    </>
  )
}

export default Base;