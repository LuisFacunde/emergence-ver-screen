import { useState } from 'react';
import './SearchForm.css';

function SearchForm({ onSearch }) {
  const [searchProntuario, setSearchProntuario] = useState('');
  const [searchNome, setSearchNome] = useState('');

  const handleSubmit = () => {
    onSearch(searchProntuario, searchNome);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="search-section">
      <div className="search-row">
        <div className="search-field">
          <input
            type="text"
            placeholder="Prontuário"
            value={searchProntuario}
            onChange={(e) => setSearchProntuario(e.target.value)}
            onKeyPress={handleKeyPress}
            className="input"
          />
          <button onClick={handleSubmit} className="btn btn-primary">
            Pesquisar
          </button>
        </div>

        <div className="search-field">
          <input
            type="text"
            placeholder="Nome"
            value={searchNome}
            onChange={(e) => setSearchNome(e.target.value)}
            onKeyPress={handleKeyPress}
            className="input"
          />
          <button onClick={handleSubmit} className="btn btn-primary">
            Pesquisar
          </button>
        </div>
      </div>
    </div>
  );
}

export default SearchForm;
