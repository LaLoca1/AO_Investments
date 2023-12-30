import React, { useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import CSRFToken from "../components/CSRFToken";

const EditWatchlistItem = ({ item, onClose }) => {
  const [editedItem, setEditedItem] = useState({
    ticker: item.ticker,
    quantity: item.quantity,
    price: item.price,
    sector: item.sector,
    trade_date: item.trade_date.split("T")[0],
    comments: item.comments,
  });

  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedItem({ ...editedItem, [name]: value });
  };

  const handleEdit = async () => {
    const config = {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
    };

    try {
      await axios.put(
        `/watchlist/api/edit-watchlist-item/${item.id}`,
        editedItem,
        config
      );
      onClose(); // Close the modal after successful edit
    } catch (error) {
      console.error("Error editing watchlist item:", error);
      setError("An error occurred while editing the item.");
    }
  };

  const handleCancel = () => {
    const confirmCancel = window.confirm(
      "Are you sure you want to cancel? Any unsaved changes will be lost."
    );
    if (confirmCancel) {
      onClose();
    }
  };

  return (
    <div className="edit-watchlist-item-container">
      <h2>Edit Watchlist Item</h2>
      <form onSubmit={handleEdit}>
        <CSRFToken />
        <label className="form-label">Ticker:</label>
        <input
          type="text"
          name="ticker"
          value={editedItem.ticker}
          onChange={handleChange}
          className="form-input"
          required
        />

        <label className="form-label">Quantity:</label>
        <input
          type="number"
          name="quantity"
          value={editedItem.quantity}
          onChange={handleChange}
          className="form-input"
          required
        />

        <label className="form-label">Price:</label>
        <input
          type="number"
          name="price"
          value={editedItem.price}
          onChange={handleChange}
          className="form-input"
          required
        />

        <label className="form-label">Sector:</label>
        <input
          type="text"
          name="sector"
          value={editedItem.sector}
          onChange={handleChange}
          className="form-input"
          required
        />

        <label className="form-label">Trade Date:</label>
        <input
          type="date"
          name="trade_date"
          value={editedItem.trade_date}
          onChange={handleChange}
          className="form-input"
          required
        />

        <label className="form-label">Comments:</label>
        <input
          type="text"
          name="comments"
          value={editedItem.comments}
          onChange={handleChange}
          className="form-input"
          required
        />

        <div className="form-buttons">
          <button type="button" onClick={handleEdit}>
            Save Changes
          </button>
          <button type="button" onClick={handleCancel}>
            Cancel
          </button>
        </div>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default EditWatchlistItem;
