/* Lib imports */
import { Link } from "react-router";

/* Components, services & etc. */
import { useAuth } from "../../services/auth/auth.provider";

/* Styling */
import "./header.component.scss";

type HeaderProps = {
    title: string
}

const Header = ({ title }: HeaderProps) => {
    const { isLoggedIn, setToken } = useAuth();
    return (
        <header>
            <nav>
                <Link className="link" to={"/"}>
                    <span id="header.title">
                        { title }
                    </span>
                </Link>
                
                <ul>
                    <li>
                        <Link className="link" to="/">Home</Link>
                    </li>
                </ul>
                {
                    !isLoggedIn ?
                        /* TODO: Get this back <Link className="login" to="/login">Login</Link> */
                        <button className="login" onClick={() => setToken({Authorization: "bla bla bla"})}>Login</button>:
                        <button className="logout" onClick={() => setToken()}>Logout</button>
                }
            </nav>
        </header>
    );
}

export default Header;