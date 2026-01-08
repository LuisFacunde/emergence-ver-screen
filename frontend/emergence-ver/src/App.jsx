import { useState } from 'react'
import Header from './components/Header'
import SearchForm from './components/SearchForm'
import Alert from './components/Alert'
import PatientTable from './components/PatientTable'
import Pagination from './components/Pagination'
import { mockPatients } from './data/mockData'
import './App.css'


function App() {
  const [patients, setPatients] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [showAlert, setShowAlert] = useState(true);
  const itemsPerPage = 10;

  const handleSearch = (prontuario, nome) => {
    if (!prontuario && !nome) {
      alert('USE OS CAMPOS ACIMA PARA PESQUISAR!\nPreencha por nome do paciente ou pelo prontuário');
      return;
    }

    let filtered = mockPatients;
    
    if (prontuario) {
      filtered = filtered.filter(p => 
        p.prontuario.includes(prontuario)
      );
    }
    
    if (nome) {
      filtered = filtered.filter(p => 
        p.nome.toLowerCase().includes(nome.toLowerCase())
      );
    }

    setPatients(filtered);
    setTotalRecords(filtered.length);
    setCurrentPage(1);
    setShowAlert(false);
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

          {showAlert && patients.length === 0 && (
            <Alert 
              type="info"
              title="USE OS CAMPOS ACIMA PARA PESQUISAR!"
              message="Preencha por nome do paciente ou pelo prontuário"
            />
          )}

          {patients.length > 0 && (
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

          {!showAlert && patients.length === 0 && (
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
