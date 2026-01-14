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
  // Buscar pacientes (Integrado com Backend)
  async searchPatients(prontuario = '', nome = '') {
    try {
      const params = new URLSearchParams();
      if (prontuario) params.append('prontuario', prontuario);
      if (nome) params.append('nome', nome);

      const response = await fetch(`${API_BASE_URL}/patients/search?${params}`);
      const result = await response.json();

      if (result.success) {
        // Mapear dados se necessário, o backend já retorna formato compatível
        return {
          success: true,
          data: result.data || [],
          total: (result.data || []).length
        };
      } else {
        console.warn('Erro na resposta da API:', result);
        // Fallback para mock se falhar (opcional, ou apenas erro)
        return {
          success: false,
          error: result.error
        };
      }
    } catch (error) {
      console.error('Erro ao buscar pacientes:', error);
      // Fallback para usuário não ficar travado durante dev sem DB
      return {
        success: false,
        error: {
          message: 'Erro de conexão. Verifique se o backend e VPN estão ativos.',
          details: error.message
        }
      };
    }
  },

  // Buscar paciente por ID (mockado - manter ou implementar logic similar se houver endpoint)
  // Por enquanto mantemos o mock para detalhes que não sejam busca, ou usamos o resultado da busca
  async getPatientById(id) {
    // Implementação simplificada reutilizando a busca se possível, ou mantendo mock
    // Como o endpoint de busca retorna todos os dados necessários, podemos simular
    await delay(300);
    const patient = mockPatients.find(p => p.id === parseInt(id));
    if (patient) return { success: true, data: patient };
    return { success: false, error: { message: 'Paciente não encontrado', code: 404 } };
  },

  async getPatientFiles(patientId, page = 1, perPage = 10, signal = null) {
    try {
      const params = new URLSearchParams();
      params.append('page', page);
      params.append('per_page', perPage);
      
      const options = signal ? { signal } : {};
      const response = await fetch(
        `${API_BASE_URL}/patients/${patientId}/files?${params}`, 
        options
      );
      const result = await response.json();
      return result;
    } catch (error) {
      // Não logar erro se foi abortado intencionalmente
      if (error.name !== 'AbortError') {
        console.error('API Error:', error);
      }
      return { success: false, error: error };
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

  async getPatientFiles(patientId) {
    try {
        const response = await fetch(`${API_BASE_URL}/patients/${patientId}/files`);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: error };
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
