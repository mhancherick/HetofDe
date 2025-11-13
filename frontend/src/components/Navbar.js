import { Link } from 'react-router-dom';
import './Navbar.css';



function Navbar() {
  return (
    <nav>
        <div className="container">
          <Link to="/">  
            <h2>Het of De?</h2>
          </Link>
            <div>
                <Link to="/">Home</Link>
                <Link to="/grammar">Grammar</Link>
                <Link to="/about">About</Link>
            </div>
        </div>
    </nav>
  );
}

export default Navbar;