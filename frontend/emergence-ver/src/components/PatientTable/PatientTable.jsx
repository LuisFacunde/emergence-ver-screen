import { useState } from 'react';
import './PatientTable.css';
import FileModal from '../FileModal';

function PatientTable({ patients }) {
  const [selectedPatient, setSelectedPatient] = useState(null);

  if (!patients || patients.length === 0) {
    return null;
  }

  const handleOpenModal = (patient) => {
    setSelectedPatient(patient);
  };

  const handleCloseModal = () => {
    setSelectedPatient(null);
  };

  return (
    <>
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>PRONTUÁRIO</th>
              <th>NOME</th>
              <th>DATA NASCIMENTO</th>
              <th>DATA ÚLTIMO ATENDIMENTO</th>
              <th>QTD EXM</th>
              <th>ÚLTIMO ATENDIMENTO</th>
              <th>VISUALIZAR</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((patient, index) => (
              <tr key={patient.prontuario || index}>
                <td>{patient.prontuario}</td>
                <td>{patient.nome}</td>
                <td>{patient.dt_nascimento || patient.dataNascimento}</td>
                <td>{patient.data_ultimo_atendimento || patient.dataUltimoAtendimento}</td>
                <td>{patient.qtd_exm || patient.qtdExm || '-'}</td>
                <td>{patient.ultimo_atendimento || patient.ultimoAtendimento}</td>
                <td>
                  <button
                    className="btn btn-view"
                    onClick={() => handleOpenModal(patient)}
                  >
                    TODOS EXAMES
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <FileModal
        isOpen={!!selectedPatient}
        onClose={handleCloseModal}
        patientId={selectedPatient?.cd_paciente || selectedPatient?.prontuario || ''}
        patientName={selectedPatient?.nome || ''}
      />
    </>
  );
}

export default PatientTable;
