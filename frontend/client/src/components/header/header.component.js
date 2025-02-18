import { Link } from "react-router-dom";
import "./header.component.scss";

const Header = ({ title }) => {
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
                    <li>
                        <Link className="link" to="/sort">Sort</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;