// Modal.js
import './Modal.css'

const Modal = ({ isOpen, children, onClose }) => {
    if (!isOpen) return null;
  
    return (
      <div className="modal-overlay">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="btn-close" onClick={onClose}></button>
            </div>
            <div className="modal-body">
              {children}
            </div>   
          </div>
        </div>
      </div>
    );
  };
  
  export default Modal;