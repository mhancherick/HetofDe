import { Link } from 'react-router-dom';
import './Navbar.css';



function Navbar() {
  return (
    <nav>
        <div className="container">
            <h2>Het of De?</h2>
            <div>
                <Link to="/">Home</Link>
                <Link to="/about">About</Link>
            </div>
        </div>
    </nav>
  );
}

export default Navbar;