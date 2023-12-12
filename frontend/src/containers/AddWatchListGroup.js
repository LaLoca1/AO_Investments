import React, { useState } from "react";
import axios from "axios";
import CSRFToken from "../components/CSRFToken";
import Cookies from "js-cookie";

const AddWatchListGroup = ({ onGroupAdded }) => {
  const [groupName, setGroupName] = useState("");

  const config = {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
  };

  const body = JSON.stringify({
    name: groupName,
  })

  const handleAddGroup = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/watchlist/api/create-watchlist-group`,
        body,
        config
      );

      if (onGroupAdded) {
        onGroupAdded(response.data);
      }
      setGroupName("");
    } catch (error) {
      console.error("Error adding watchlist group:", error);
    }
  };

  return (
    <div>
      <h2>Add Watchlist Group</h2>
      <form onSubmit={handleAddGroup}>
        <CSRFToken />
        <label>Group Name:</label>
        <input
          type="text"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          required
        />
        <button type="submit">Add Group</button>
      </form>
    </div>
    
  );
};

export default AddWatchListGroup;
