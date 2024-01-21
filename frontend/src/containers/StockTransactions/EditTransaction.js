import React, { useState } from "react";
import './EditTransaction.css';

const EditTransaction = ({ item, onSave, onCancel }) => {
  const [editedItem, setEditedItem] = useState({ ...item });

  const handleChange = (e) => {
    setEditedItem({ ...editedItem, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(editedItem);
  };

  return (
    <div className="edit-popup">
      <h2>Edit Transaction</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Ticker:
          <input
            type="text"
            name="ticker"
            value={editedItem.ticker}
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
          Price(£):
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

export default EditTransaction;
