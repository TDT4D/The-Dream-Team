/* Lib imports */
import { Link } from "react-router";

/* Styling */
import "./header.component.scss";

type HeaderProps = {
    title: string
}

const Header = ({ title }: HeaderProps) => {
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

                <Link className="login" to="/login">Login</Link>
            </nav>
        </header>
    );
}

export default Header;