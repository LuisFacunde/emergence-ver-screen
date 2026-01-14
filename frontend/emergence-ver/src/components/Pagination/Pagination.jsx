import './Pagination.css';

function Pagination({ 
  currentPage, 
  totalPages, 
  totalRecords,
  startIndex,
  itemsPerPage,
  onPrevious, 
  onNext 
}) {
  if (totalRecords === 0) {
    return null;
  }

  return (
    <>
      {/* Pagination Info */}
      <div className="pagination-info">
        Mostrando {startIndex + 1} de {totalRecords} ({totalRecords} total)
        <div className="pagination-controls">
          <span>Pesquisar</span>
          <input 
            type="number" 
            value={currentPage} 
            readOnly 
            className="page-input" 
          />
          <span>/ {totalPages} pág.</span>
        </div>
      </div>

      {/* Pagination Buttons */}
      <div className="pagination">
        <button 
          onClick={onPrevious}
          disabled={currentPage === 1}
          className="btn btn-pagination"
        >
          Anterior
        </button>
        <span className="page-number">{currentPage}</span>
        <button 
          onClick={onNext}
          disabled={currentPage === totalPages}
          className="btn btn-pagination"
        >
          Próxima
        </button>
      </div>
    </>
  );
}

export default Pagination;
