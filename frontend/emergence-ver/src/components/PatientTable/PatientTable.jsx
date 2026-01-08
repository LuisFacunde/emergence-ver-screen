import './PatientTable.css';

function PatientTable({ patients }) {
  if (!patients || patients.length === 0) {
    return null;
  }

  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            <th>PRONTUÁRIO</th>
            <th>NOME</th>
            <th>DATA NASCIMENTO</th>
            <th>ÚLTIMO ATENDIMENTO</th>
            <th>QTD EXM</th>
            <th>DATA ÚLTIMO ATENDIMENTO</th>
            <th>PRESTADOR</th>
            <th>VISUALIZAR</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id}>
              <td>{patient.prontuario}</td>
              <td>{patient.nome}</td>
              <td>{patient.dataNascimento}</td>
              <td>{patient.ultimoAtendimento}</td>
              <td>{patient.qtdExm}</td>
              <td>{patient.dataUltimoAtendimento}</td>
              <td>{patient.prestador}</td>
              <td>
                <button className="btn btn-view">
                  TODOS ATENDIMENTOS
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PatientTable;
