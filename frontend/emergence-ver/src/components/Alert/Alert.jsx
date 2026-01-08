import './Alert.css';

function Alert({ type = 'info', title, message }) {
  const getIcon = () => {
    switch (type) {
      case 'error':
        return '✗';
      case 'success':
        return '✓';
      case 'warning':
        return '⚠';
      default:
        return '✓';
    }
  };

  return (
    <div className={`alert alert-${type}`}>
      <span className="alert-icon">{getIcon()}</span>
      <div>
        {title && <strong>{title}</strong>}
        {message && <p>{message}</p>}
      </div>
    </div>
  );
}

export default Alert;
