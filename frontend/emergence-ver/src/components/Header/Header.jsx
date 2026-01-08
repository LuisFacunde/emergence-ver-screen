import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <div className="logo-text">FAV</div>
          <div className="logo-subtitle">Fundação Altino Ventura</div>
        </div>
        <nav className="nav">
          <a href="#" className="nav-link">VOLTAR</a>
          <a href="#" className="nav-link">INÍCIO</a>
        </nav>
      </div>
    </header>
  );
}

export default Header;
