import React, { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

const DisplayWatchlist = () => {
  const [watchlistItems, setWatchlistItems] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get("/watchlist/api/user/watchlist-items");
      setWatchlistItems(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleDelete = async (id) => {
    const config = {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
    };

    try {
      await axios.delete(`/watchlist/api/delete-watchlist-item/${id}`, config);
      // Refresh the watchlist after deletion
      fetchData();
    } catch (error) {
      console.error("Error deleting watchlist item:", error);
    }
  };

  return (
    <div>
      <h1>Watchlist Items</h1>
      <ul>
        {watchlistItems.map((item) => (
          <li key={item.id}>
            {item.id} - {item.ticker} - {item.quantity} - {item.price} -{" "}
            {item.sector} - {new Date(item.trade_date).toLocaleDateString()} -{" "}
            {item.comments}
            <button onClick={() => handleDelete(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DisplayWatchlist;
