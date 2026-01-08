// API Service - Preparado para integração futura com backend Flask
// Por enquanto, retorna dados mockados

const API_BASE_URL = 'http://localhost:5000/api';

// Dados mockados
const mockPatients = [
  {
    id: 1,
    prontuario: '2345170',
    nome: 'LUIS HENRIQUE FACCINI DA SILVA',
    dataNascimento: '19/06/2001',
    ultimoAtendimento: '7464880',
    qtdExm: 1,
    dataUltimoAtendimento: '16/06/2025',
    prestador: 'INGRID PINTO TORRES'
  },
  {
    id: 2,
    prontuario: '1234567',
    nome: 'MARIA SANTOS OLIVEIRA',
    dataNascimento: '15/03/1985',
    ultimoAtendimento: '7464881',
    qtdExm: 3,
    dataUltimoAtendimento: '20/12/2025',
    prestador: 'DR. CARLOS MENDES'
  },
  {
    id: 3,
    prontuario: '9876543',
    nome: 'JOÃO PEDRO ALMEIDA',
    dataNascimento: '22/07/1990',
    ultimoAtendimento: '7464882',
    qtdExm: 2,
    dataUltimoAtendimento: '18/11/2025',
    prestador: 'DRA. ANA PAULA'
  },
  {
    id: 4,
    prontuario: '5551234',
    nome: 'FERNANDA COSTA RIBEIRO',
    dataNascimento: '10/09/1978',
    ultimoAtendimento: '7464883',
    qtdExm: 5,
    dataUltimoAtendimento: '25/10/2025',
    prestador: 'DR. ROBERTO SILVA'
  },
  {
    id: 5,
    prontuario: '7778889',
    nome: 'CARLOS EDUARDO MARTINS',
    dataNascimento: '05/12/1995',
    ultimoAtendimento: '7464884',
    qtdExm: 1,
    dataUltimoAtendimento: '30/09/2025',
    prestador: 'DRA. JULIANA ROCHA'
  },
  {
    id: 6,
    prontuario: '3334445',
    nome: 'ANA BEATRIZ SOUZA',
    dataNascimento: '18/04/1988',
    ultimoAtendimento: '7464885',
    qtdExm: 4,
    dataUltimoAtendimento: '12/08/2025',
    prestador: 'DR. MARCOS ANTONIO'
  },
  {
    id: 7,
    prontuario: '6667778',
    nome: 'PEDRO HENRIQUE LIMA',
    dataNascimento: '25/11/1992',
    ultimoAtendimento: '7464886',
    qtdExm: 2,
    dataUltimoAtendimento: '05/07/2025',
    prestador: 'DRA. PATRICIA GOMES'
  },
  {
    id: 8,
    prontuario: '8889990',
    nome: 'JULIANA FERREIRA COSTA',
    dataNascimento: '30/01/1980',
    ultimoAtendimento: '7464887',
    qtdExm: 6,
    dataUltimoAtendimento: '22/06/2025',
    prestador: 'DR. RICARDO SANTOS'
  }
];

// Simula delay de rede
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// API Service
const apiService = {
  // Buscar pacientes (mockado)
  async searchPatients(prontuario = '', nome = '') {
    // Simula delay de rede
    await delay(500);

    // Filtrar dados mockados
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

    return {
      success: true,
      data: filtered,
      total: filtered.length
    };
  },

  // Buscar paciente por ID (mockado)
  async getPatientById(id) {
    await delay(300);
    
    const patient = mockPatients.find(p => p.id === parseInt(id));
    
    if (patient) {
      return {
        success: true,
        data: patient
      };
    } else {
      return {
        success: false,
        error: {
          message: 'Paciente não encontrado',
          code: 404
        }
      };
    }
  },

  // ===== FUNÇÕES PREPARADAS PARA INTEGRAÇÃO FUTURA =====
  // Descomente quando o backend estiver pronto

  /*
  // Buscar pacientes via API real
  async searchPatientsAPI(prontuario = '', nome = '') {
    try {
      const params = new URLSearchParams();
      if (prontuario) params.append('prontuario', prontuario);
      if (nome) params.append('nome', nome);

      const response = await fetch(`${API_BASE_URL}/patients?${params}`);
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error('Erro ao buscar pacientes:', error);
      return {
        success: false,
        error: {
          message: 'Erro ao conectar com o servidor',
          code: 500
        }
      };
    }
  },

  // Buscar paciente por ID via API real
  async getPatientByIdAPI(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/patients/${id}`);
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error('Erro ao buscar paciente:', error);
      return {
        success: false,
        error: {
          message: 'Erro ao conectar com o servidor',
          code: 500
        }
      };
    }
  },

  // Criar novo paciente
  async createPatient(patientData) {
    try {
      const response = await fetch(`${API_BASE_URL}/patients`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData)
      });
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error('Erro ao criar paciente:', error);
      return {
        success: false,
        error: {
          message: 'Erro ao conectar com o servidor',
          code: 500
        }
      };
    }
  },

  // Atualizar paciente
  async updatePatient(id, patientData) {
    try {
      const response = await fetch(`${API_BASE_URL}/patients/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData)
      });
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error('Erro ao atualizar paciente:', error);
      return {
        success: false,
        error: {
          message: 'Erro ao conectar com o servidor',
          code: 500
        }
      };
    }
  },

  // Deletar paciente
  async deletePatient(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/patients/${id}`, {
        method: 'DELETE'
      });
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error('Erro ao deletar paciente:', error);
      return {
        success: false,
        error: {
          message: 'Erro ao conectar com o servidor',
          code: 500
        }
      };
    }
  }
  */
};

export default apiService;
