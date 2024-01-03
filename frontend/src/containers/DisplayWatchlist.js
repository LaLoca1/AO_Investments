import React, { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import EditWatchlistItem from "./EditWatchlistItem"; // Import your new component

const DisplayWatchlist = () => {
  const [watchlistItems, setWatchlistItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingItem, setEditingItem] = useState(null);

  const handleEdit = (item) => {
    setEditingItem(item);
  };

  const handleSaveEdit = async (editedItem) => {
    const config = {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
    };

    try {
      const response = await axios.put(
        `/watchlist/api/edit-watchlist-item/${editedItem.id}`,
        editedItem,
        config
      );

      if (response.status === 200) {
        setWatchlistItems((prevItems) =>
          prevItems.map((item) =>
            item.id === editedItem.id ? editedItem : item
          )
        );

        setEditingItem(null);
      }
    } catch (error) {
      console.error("Error updating watchlist item:", error);
    }
  };

  const handleCancelEdit = () => {
    setEditingItem(null);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/watchlist/api/user/watchlist-items");
      setWatchlistItems(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    // Add a confirmation dialog before deletion
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this item?"
    );
    if (!confirmDelete) {
      return;
    }

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
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {watchlistItems.map((item) => (
            <li key={item.id}>
              {item.id} - {item.ticker} - {item.quantity} - {item.price} -{" "}
              {item.sector} - {new Date(item.trade_date).toLocaleDateString()} -{" "}
              {item.comments} - {item.transactionType}
              <button onClick={() => handleEdit(item)}>Edit</button>
              <button onClick={() => handleDelete(item.id)}>Delete</button>
            </li>
          ))}
          {editingItem && (
            <EditWatchlistItem 
            item={editingItem} 
            onSave={handleSaveEdit} 
            onCancel={handleCancelEdit}
            /> 
          )} 
        </ul>
      )}
    </div>
  );
};

export default DisplayWatchlist;
