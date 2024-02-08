import React, { useState } from "react";
import './EditTransaction.css';

const EditCryptoTransaction = ({ item, onSave, onCancel }) => {
  const [editedItem, setEditedItem] = useState({ ...item });

  const validateInput = () => {
    if (parseInt(editedItem.quantity) < 0 ) {
      alert("Quantity must be positive.");
      return false;
    }

    if (parseInt(editedItem.price) < 0 ) {
      alert("Price must be positive.");
      return false;
    }
    return true;
  };

  const handleChange = (e) => {
    setEditedItem({ ...editedItem, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validateInput()) {
      return; 
    }
    onSave(editedItem);
  };

  return (
    <div className="edit-popup">
      <h2>Edit Transaction</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Coin:
          <input
            type="text"
            name="coin"
            value={editedItem.coin}
            onChange={handleChange}
          />
        </label>

        <label>
          Quantity:
          <input
            type="number"
            name="quantity"
            value={editedItem.quantity}
            onChange={handleChange}
          />
        </label>

        <label>
          Price($):
          <input
            type="number"
            name="price"
            value={editedItem.price}
            onChange={handleChange}
          />
        </label>

        <label>
          Sector:
          <input
            type="text"
            name="sector"
            value={editedItem.sector}
            onChange={handleChange}
          />
        </label>
        
        <label>
          Trade Date:
          <input
            type="date"
            name="trade_date"
            value={new Date(editedItem.trade_date).toISOString().split("T")[0]}
            onChange={handleChange}
          />
        </label>

        <label>
          Comments:
          <textarea
            name="comments"
            value={editedItem.comments}
            onChange={handleChange}
          />
        </label>
        
        <div className="form-buttons">
          <button type="submit">Save</button>
          <button onClick={onCancel}>Cancel</button>
        </div>
      </form>
    </div>
  );
};

export default EditCryptoTransaction;
