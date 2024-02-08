import React, { useState } from "react";
import CSRFToken from "../../components/CSRFToken";
import './AddTransaction.css'

const AddCryptoTransaction = ({ onItemAdded }) => {
  const [coin, setCoin] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [fees, setFees] = useState("");
  const [tradeDate, setTradeDate] = useState("");
  const [comments, setComments] = useState(""); // New state for comments
  const [transactionType, setTransactionType] = useState("");

  const validateInput = () => {
    if (parseInt(quantity) < 0 ) {
      alert("Quantity must be positive.");
      return false;
    }

    if (parseInt(price) < 0 ) {
      alert("Price must be positive.");
      return false;
    }

    if (parseInt(quantity) < 0 && parseInt(price) < 0 ) {
      alert("Quantity and Price must be positive.");
      return false;
    }

    if (transactionType.toLowerCase() !== "buy" && transactionType.toLowerCase() !== "sell") {
      alert("Please enter a valid transaction type (Buy or Sell).");
      return false;
  }
    return true;
  };

  const handleAddItem = async (e) => {
    e.preventDefault();

    if (!validateInput()) {
      return; 
    }

    const newItem = {
      coin,
      quantity: parseInt(quantity), 
      price: parseFloat(price), 
      fees,
      trade_date: tradeDate,
      comments,
      transactionType,
    };

    onItemAdded(newItem);

    setCoin("");
    setQuantity("");
    setPrice("");
    setFees("");
    setTradeDate("");
    setComments("");
    setTransactionType("");
  };

  return (
    <div className="add-transaction-form">
      <h2>Add Transaction</h2>
      <form onSubmit={handleAddItem}>
        <CSRFToken />
        <label>Coin:</label>
        <input
          type="text"
          value={coin}
          onChange={(e) => setCoin(e.target.value)}
          required
        />

        <label>Quantity:</label>
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          required
        />

        <label>Price($):</label>
        <input
          type="number"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />

        <label>Fees($):</label>
        <input
          type="number"
          value={fees}
          onChange={(e) => setFees(e.target.value)}
          required
        />

        <label>Trade Date:</label>
        <input
          type="date"
          value={tradeDate}
          onChange={(e) => setTradeDate(e.target.value)}
          required
        />
        
        <label>Comments:</label>
        <input
          type="text"
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          required
        />

        <label>Transaction Type(Buy/Sell):</label>
        <input
          type="text"
          value={transactionType}
          onChange={(e) => setTransactionType(e.target.value)}
          required
        />
        <button type="submit">Add Item</button>
      </form>
    </div>
  );
};

export default AddCryptoTransaction;
