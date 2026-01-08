import { useState, useEffect } from 'react';
import apiService from '../../services/api';
import './FileModal.css';

function FileModal({ isOpen, onClose, patientId, patientName }) {
    const [fileList, setFileList] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (isOpen && patientId) {
            setIsLoading(true);
            setError(null);
            setFileList([]);

            apiService.getPatientFiles(patientId)
                .then(result => {
                    if (result.success) {
                        setFileList(result.data || []);
                    } else {
                        setError('Erro ao carregar arquivos.');
                    }
                })
                .catch(() => setError('Erro de conexão.'))
                .finally(() => setIsLoading(false));
        }
    }, [isOpen, patientId]);

    if (!isOpen) return null;

    return (
        <div className="file-modal-overlay" onClick={onClose}>
            <div className="file-modal-content" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2 className="modal-title">Arquivos - {patientName}</h2>
                    <button className="modal-close" onClick={onClose}>&times;</button>
                </div>

                <div className="modal-body">
                    {isLoading ? (
                        <div className="modal-loading">
                            <div className="spinner-small"></div>
                            <p>Buscando arquivos...</p>
                        </div>
                    ) : error ? (
                        <div className="modal-error">{error}</div>
                    ) : (Array.isArray(fileList) && fileList.length > 0) ? (
                        <ul className="file-list">
                            {fileList
                                .sort((a, b) => {
                                    if (!a || !b) return 0;
                                    // Tentar ordenar pela data no nome do arquivo (descrescente)
                                    // Padrão esperado agora: ...-YYYYMMDD-...
                                    const getDate = (name) => {
                                        if (!name) return 0;
                                        try {
                                            const parts = name.split('-');
                                            if (parts.length >= 3) {
                                                const dateStr = parts[2];
                                                // Formato YYYYMMDD
                                                if (dateStr && dateStr.length === 8 && !isNaN(dateStr)) {
                                                    const year = dateStr.substring(0, 4);
                                                    const month = dateStr.substring(4, 6);
                                                    const day = dateStr.substring(6, 8);
                                                    return new Date(`${year}-${month}-${day}`).getTime(); // timestamp for safe sub
                                                }
                                            }
                                        } catch (e) { return 0; }
                                        return 0; // fallback
                                    };

                                    const dateA = getDate(a.name) || 0;
                                    const dateB = getDate(b.name) || 0;

                                    // Se tem datas diferentes, ordena
                                    if (dateA !== dateB) return dateB - dateA;

                                    // Fallback para data de modificação
                                    return (b.date || 0) - (a.date || 0);
                                })
                                .map((file, index) => {
                                    if (!file || !file.name) return null; // Proteção contra arquivos inválidos

                                    // Extrair data para exibição (Formatando para DD/MM/YYYY)
                                    let displayDate = "";
                                    try {
                                        const parts = file.name.split('-');
                                        if (parts.length >= 3) {
                                            const dateStr = parts[2];
                                            if (dateStr && dateStr.length === 8 && !isNaN(dateStr)) {
                                                const year = dateStr.substring(0, 4);
                                                const month = dateStr.substring(4, 6);
                                                const day = dateStr.substring(6, 8);
                                                displayDate = `${day}/${month}/${year}`;
                                            }
                                        }
                                    } catch (e) { }

                                    return (
                                        <li key={index} className="file-item">
                                            <span className="file-icon">📄</span>
                                            <div className="file-actions">
                                                <div className="file-info-col">
                                                    <a
                                                        href={`http://localhost:5000/api/files/download?path=${encodeURIComponent(file.path || '')}&name=${file.name}`}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="file-name"
                                                        title={`Arquivo original: ${file.name}`}
                                                    >
                                                        {file.display_name || file.name}
                                                    </a>
                                                    {file.eye && (
                                                        <span className={`eye-badge eye-${String(file.eye).toLowerCase()}`} title={file.eye === 'OD' ? 'Olho Direito' : file.eye === 'OE' ? 'Olho Esquerdo' : 'Ambos os Olhos'}>
                                                            {file.eye}
                                                        </span>
                                                    )}
                                                </div>

                                                <div className="file-meta">
                                                    {displayDate && <span className="file-date">{displayDate}</span>}
                                                    <a
                                                        href={`http://localhost:5000/api/files/download?path=${encodeURIComponent(file.path || '')}&name=${file.name}&download=true`}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="btn-download"
                                                        title="Baixar Arquivo"
                                                    >
                                                        ⬇️
                                                    </a>
                                                </div>
                                            </div>
                                        </li>
                                    )
                                })}
                        </ul>
                    ) : (
                        <div className="no-files">Nenhum arquivo encontrado para este paciente.</div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default FileModal;
