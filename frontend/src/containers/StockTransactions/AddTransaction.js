import React, { useState } from "react";
import CSRFToken from "../../components/CSRFToken";

const AddTransaction = ({ onItemAdded }) => {
  const [ticker, setTicker] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [sector, setSector] = useState("");
  const [market, setMarket] = useState("");
  const [tradeDate, setTradeDate] = useState("");
  const [comments, setComments] = useState(""); // New state for comments
  const [transactionType, setTransactionType] = useState("");

  const handleAddItem = async (e) => {
    e.preventDefault();

    const newItem = {
      ticker,
      quantity,
      price,
      sector,
      market,
      trade_date: tradeDate,
      comments,
      transactionType,
    };

    onItemAdded(newItem);

    setTicker("");
    setQuantity("");
    setPrice("");
    setSector("");
    setMarket("");
    setTradeDate("");
    setComments("");
    setTransactionType("");
  };

  return (
    <div>
      <h2>Add Watchlist Item</h2>
      <form onSubmit={handleAddItem}>
        <CSRFToken />
        <label>Ticker:</label>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          required
        />

        <label>Quantity:</label>
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          required
        />

        <label>Price(£):</label>
        <input
          type="number"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />

        <label>Sector:</label>
        <input
          type="text"
          value={sector}
          onChange={(e) => setSector(e.target.value)}
          required
        />

        <label>Market(UK/US):</label>
        <input
          type="text"
          value={market}
          onChange={(e) => setMarket(e.target.value)}
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

export default AddTransaction;
