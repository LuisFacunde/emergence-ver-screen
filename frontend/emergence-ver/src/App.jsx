import { useState } from 'react'
import Header from './components/Header'
import SearchForm from './components/SearchForm'
import Alert from './components/Alert'
import PatientTable from './components/PatientTable'
import Pagination from './components/Pagination'
import apiService from './services/api';

function App() {
  const [patients, setPatients] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [showAlert, setShowAlert] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const itemsPerPage = 10;

  const handleSearch = async (prontuario, nome) => {
    if (!prontuario && !nome) {
      alert('USE OS CAMPOS ACIMA PARA PESQUISAR!\nPreencha por nome do paciente ou pelo prontuário');
      return;
    }

    setIsLoading(true);
    setCurrentPage(1);

    try {
      const result = await apiService.searchPatients(prontuario, nome);

      if (result.success) {
        setPatients(result.data);
        setTotalRecords(result.data.length);
      } else {
        console.error("Erro na busca:", result.error);
        alert(`Erro na busca: ${result.error?.message || 'Erro desconhecido'}`);
        setPatients([]);
        setTotalRecords(0);
      }
    } catch (error) {
      console.error("Erro inesperado:", error);
      alert("Erro inesperado ao buscar pacientes.");
      setPatients([]);
      setTotalRecords(0);
    } finally {
      setIsLoading(false);
      setShowAlert(false);
    }
  };

  const totalPages = Math.ceil(totalRecords / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentPatients = patients.slice(startIndex, endIndex);

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <div className="app">
      <Header />

      <main className="main-content">
        <div className="container">
          <div className="page-title">
            <span className="icon">☰</span> PESQUISA DE PACIENTES
          </div>

          <SearchForm onSearch={handleSearch} />

          {isLoading && (
            <div className="loading-overlay">
              <div className="spinner"></div>
              <p>Carregando pacientes e arquivos...</p>
            </div>
          )}

          {showAlert && patients.length === 0 && !isLoading && (
            <Alert
              type="info"
              title="USE OS CAMPOS ACIMA PARA PESQUISAR!"
              message="Preencha por nome do paciente ou pelo prontuário"
            />
          )}

          {patients.length > 0 && !isLoading && (
            <>
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                totalRecords={totalRecords}
                startIndex={startIndex}
                itemsPerPage={itemsPerPage}
                onPrevious={handlePreviousPage}
                onNext={handleNextPage}
              />

              <PatientTable patients={currentPatients} />

              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                totalRecords={totalRecords}
                startIndex={startIndex}
                itemsPerPage={itemsPerPage}
                onPrevious={handlePreviousPage}
                onNext={handleNextPage}
              />
            </>
          )}

          {!showAlert && patients.length === 0 && !isLoading && (
            <div className="no-results">
              Nenhum paciente encontrado com os critérios informados.
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
