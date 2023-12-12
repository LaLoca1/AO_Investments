import React, { useEffect, useState } from "react";
import axios from "axios";
import CSRFToken from "../components/CSRFToken";
import Cookies from "js-cookie";

const AddWatchlistItem = ({ onItemAdded }) => {
  const [ticker, setTicker] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [sector, setSector] = useState("");
  const [tradeDate, setTradeDate] = useState("");
  const [comments, setComments] = useState(""); // New state for comments
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await axios.get("/watchlist/api/watchlist-groups");
        setGroups(response.data);
      } catch (error) {
        console.error("Error fetching groups:", error);
      }
    };

    fetchGroups();
  }, []);

  const config = {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
  };

  const body = JSON.stringify({
    ticker,
    quantity,
    price,
    sector,
    trade_date: tradeDate,
    comments, // Include comments in the request
    group: selectedGroup || null,
  });

  const handleAddItem = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/watchlist/api/create-watchlist-item`,
        body,
        config
      );

      if (onItemAdded) {
        onItemAdded(response.data);
      }

      setTicker("");
      setQuantity("");
      setPrice("");
      setSector("");
      setTradeDate("");
      setComments(""); // Clear the comments field
      setSelectedGroup(null);
    } catch (error) {
      console.error("Error adding watchlist item:", error);
    }
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

        <label>Price:</label>
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

        <label>Trade Date:</label>
        <input
          type="date"
          value={tradeDate}
          onChange={(e) => setTradeDate(e.target.value)}
          required
        />

        {/* The new "Comments" field */}
        <label>Comments:</label>
        <input
          type="text"
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          required
        />

        {/* The existing dropdown for selecting a group */}
        <label>Group:</label>
        <select
          value={selectedGroup}
          onChange={(e) => setSelectedGroup(e.target.value)}
        >
          <option value="" disabled>
            Select a group
          </option>
          {groups.map((group) => (
            <option key={group.id} value={group.id}>
              {group.name}
            </option>
          ))}
        </select>

        <button type="submit">Add Item</button>
      </form>
    </div>
  );
};

export default AddWatchlistItem;