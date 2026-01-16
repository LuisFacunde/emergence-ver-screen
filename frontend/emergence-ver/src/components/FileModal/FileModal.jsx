import { useState, useEffect, useRef } from 'react';
import { Modal, List, Button, Tag, Tooltip, Image, Spin, Typography, Space } from 'antd';
import { DownloadOutlined, EyeOutlined, FilePdfOutlined, FileImageOutlined } from '@ant-design/icons';
import Draggable from 'react-draggable';
import apiService from '../../services/api';
import './FileModal.css';

const { Text, Paragraph } = Typography;
const ITEMS_PER_PAGE = 10;

// Wrapper componente to providing nodeRef to Draggable
const DraggableModalWrapper = ({ modal, id, onFocus }) => {
    const dragRef = useRef(null);
    const [dragging, setDragging] = useState(false);

    return (
        <Draggable
            nodeRef={dragRef}
            disabled={false}
            handle=".ant-modal-header"
            onMouseDown={() => onFocus(id)}
            onStart={() => setDragging(true)}
            onStop={() => setDragging(false)}
        >
            <div
                ref={dragRef}
                style={{ pointerEvents: 'auto', position: 'relative' }}
            >
                {modal}
                {dragging && (
                    <div style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        zIndex: 9999,
                        background: 'transparent'
                    }} />
                )}
            </div>
        </Draggable>
    );
};

function FileModal({ isOpen, onClose, patientId, patientName }) {
    const [fileList, setFileList] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [total, setTotal] = useState(0);

    // Array para previews acumulativos
    const [activePreviews, setActivePreviews] = useState([]);
    const [zIndexCounter, setZIndexCounter] = useState(1000);

    const abortControllerRef = useRef(null);

    const loadFiles = async (currentPage) => {
        if (!patientId) return;

        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }

        setIsLoading(true);
        abortControllerRef.current = new AbortController();

        try {
            const result = await apiService.getPatientFiles(
                patientId,
                currentPage,
                ITEMS_PER_PAGE,
                abortControllerRef.current.signal
            );

            if (result.success) {
                setFileList(result.data.files || []);
                setTotal(result.data.pagination?.total_files || 0);
                setPage(currentPage);
            }
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error("Erro ao carregar arquivos:", err);
            }
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isOpen && patientId) {
            loadFiles(1);
        } else {
            setFileList([]);
            setPage(1);
            setTotal(0);
            setActivePreviews([]);
        }
        return () => {
            if (abortControllerRef.current) abortControllerRef.current.abort();
        };
    }, [isOpen, patientId]);

    const handlePreview = (file) => {
        if (!file) return;

        const fileUrl = `http://localhost:5000/api/files/download?path=${encodeURIComponent(file.path || '')}&name=${file.name}`;
        const isPdf = file.name ? file.name.toLowerCase().endsWith('.pdf') : false;

        const previewId = `${file.name || 'unknown'}-${Date.now()}`;
        const newZIndex = zIndexCounter + 1;
        setZIndexCounter(newZIndex);

        setActivePreviews(prev => [...prev, {
            id: previewId,
            uniqueKey: previewId,
            url: fileUrl,
            title: file.display_name || file.name || 'Sem título',
            type: isPdf ? 'pdf' : 'image',
            zIndex: newZIndex,
            file: file
        }]);
    };

    const closePreview = (id) => {
        setActivePreviews(prev => prev.filter(p => p.id !== id));
    };

    const bringToFront = (id) => {
        setZIndexCounter(prev => {
            const newZ = prev + 1;
            setActivePreviews(list => list.map(p =>
                p.id === id ? { ...p, zIndex: newZ } : p
            ));
            return newZ;
        });
    };

    const formatDate = (timestamp) => {
        if (!timestamp) return '-';
        return new Date(timestamp * 1000).toLocaleDateString('pt-BR');
    };

    const renderItem = (file) => {
        if (!file) return null;
        const isPdf = file.name ? file.name.toLowerCase().endsWith('.pdf') : false;

        return (
            <List.Item
                actions={[
                    <Tooltip key="view" title="Visualizar (Nova Janela)">
                        <Button
                            icon={<EyeOutlined />}
                            onClick={() => handlePreview(file)}
                        />
                    </Tooltip>,
                    <Tooltip key="download" title="Baixar">
                        <Button
                            icon={<DownloadOutlined />}
                            href={`http://localhost:5000/api/files/download?path=${encodeURIComponent(file.path || '')}&name=${file.name}&download=true`}
                            target="_blank"
                        />
                    </Tooltip>
                ]}
            >
                <List.Item.Meta
                    avatar={isPdf ? <FilePdfOutlined style={{ fontSize: 24, color: '#f5222d' }} /> : <FileImageOutlined style={{ fontSize: 24, color: '#1890ff' }} />}
                    title={
                        <Space>
                            <Text strong onClick={() => handlePreview(file)} style={{ cursor: 'pointer', color: '#1890ff' }}>
                                {file.display_name || file.name}
                            </Text>
                            {file.eye && (
                                <Tag color={file.eye === 'OD' ? 'blue' : file.eye === 'OE' ? 'green' : 'purple'}>
                                    {file.eye}
                                </Tag>
                            )}
                            <Text type="secondary" style={{ fontSize: '12px' }}>
                                {formatDate(file.date)}
                            </Text>
                        </Space>
                    }
                    description={
                        <div>
                            {file.observation && (
                                <Paragraph style={{ margin: 0 }} type="secondary" ellipsis={{ rows: 2, expandable: true, symbol: 'more' }}>
                                    Obs: {file.observation}
                                </Paragraph>
                            )}
                            <Text type="secondary" style={{ fontSize: '11px' }}>{file.name}</Text>
                        </div>
                    }
                />
            </List.Item>
        );
    };

    return (
        <>
            {/* Modal Principal (Lista) */}
            <Modal
                title={`Arquivos - ${patientName}`}
                open={isOpen}
                onCancel={onClose}
                footer={null}
                width={800}
                style={{ top: 20 }}
                mask={true} // Bloqueia clicks fora
            >
                {isLoading && !fileList.length ? (
                    <div style={{ textAlign: 'center', padding: '20px' }}><Spin size="large" /></div>
                ) : (
                    <List
                        itemLayout="horizontal"
                        dataSource={fileList}
                        renderItem={renderItem}
                        pagination={{
                            current: page,
                            pageSize: ITEMS_PER_PAGE,
                            total: total,
                            onChange: (p) => loadFiles(p),
                            showSizeChanger: false
                        }}
                        locale={{ emptyText: 'Nenhum arquivo encontrado' }}
                    />
                )}
            </Modal>

            {/* Modais de Preview (Acumulativos) */}
            {activePreviews.map((preview, index) => (
                <Modal
                    key={preview.uniqueKey}
                    title={
                        <div
                            style={{ width: '100%', cursor: 'move' }}
                        >
                            {preview.title}
                        </div>
                    }
                    open={true}
                    onCancel={() => closePreview(preview.id)}
                    footer={null}
                    width={500}
                    wrapClassName="draggable-modal-wrapper"
                    mask={false} // PERMITE INTERAÇÃO COM OUTRAS JANELAS
                    maskClosable={false} // Impede fechar ao clicar "fora" (necessário mesmo sem mask visível)
                    keyboard={false} // Opcional: impede fechar com ESC para evitar acidentes
                    style={{
                        top: 50 + (index * 30),
                        left: (index * 30)
                    }}
                    zIndex={preview.zIndex}
                    modalRender={(modal) => {
                        // Uso direto do Draggable com nodeRef e bounds 'parent' ou removido para evitar erros
                        return (
                            <DraggableModalWrapper
                                modal={modal}
                                id={preview.id}
                                onFocus={bringToFront}
                            />
                        );
                    }}
                >
                    <div
                        style={{ height: '500px', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f0f2f5', overflow: 'hidden' }}
                    >
                        {preview.type === 'pdf' ? (
                            <iframe
                                src={preview.url}
                                style={{ width: '100%', height: '100%', border: 'none' }}
                                title={`PDF Preview ${preview.id}`}
                            />
                        ) : (
                            <Image
                                src={preview.url}
                                style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                                preview={false}
                            />
                        )}
                    </div>
                </Modal>
            ))}
        </>
    );
}

export default FileModal;
