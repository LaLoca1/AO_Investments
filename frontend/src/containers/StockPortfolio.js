import React, { useState, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import DisplayWatchlist from "./DisplayWatchlist";
import AddWatchlistItem from "./AddWatchlistItem";
import EditWatchlistItem from "./EditWatchlistItem";
import DisplayPortfolio from "./DisplayPortfolio";

const StockPortfolio = () => {
  const [watchlistItems, setWatchlistItems] = useState([]);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [refreshCounter, setRefreshCounter] = useState(0);

  // Fetch watchlist items on component mount
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/watchlist/api/user/transaction-items");
      setWatchlistItems(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    setRefreshCounter(c => c + 1);
    fetchData();
  };

  const handleAddItem = async (newItem) => {
    const config = {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
    };

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/watchlist/api/create-transaction-item`,
        newItem,
        config
      );

      if (response.status === 201) {
        // Update the watchlist items state here
        fetchData();
        refreshData(); 
      }
    } catch (error) {
      console.error("Error adding watchlist item:", error);
    }
  };

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
        `/watchlist/api/edit-transaction-item/${editedItem.id}`,
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
      await axios.delete(`/watchlist/api/delete-transaction-item/${id}`, config);
      // Refresh the watchlist after deletion
      fetchData();
      refreshData(); 
    } catch (error) {
      console.error("Error deleting watchlist item:", error);
    }
  };

  const filteredItems = filter
    ? watchlistItems.filter((item) =>
        item.ticker.toLowerCase().includes(filter.toLowerCase())
      )
    : watchlistItems;

  return (
    <div>
      <DisplayPortfolio key={refreshCounter} />
      <button onClick={() => setShowAddForm(!showAddForm)}>Add Item</button>
      {showAddForm && <AddWatchlistItem onItemAdded={handleAddItem} />}
      <DisplayWatchlist
        items={filteredItems}
        filter={filter}
        setFilter={setFilter}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
      {editingItem && (
        <EditWatchlistItem
          item={editingItem}
          onSave={handleSaveEdit}
          onCancel={handleCancelEdit}
        />
      )}
    </div>
  );
};
export default StockPortfolio;
