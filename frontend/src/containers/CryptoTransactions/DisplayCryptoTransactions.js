import React, { useState, useMemo } from "react";

const DisplayCryptoTransactions = ({ items, filter, setFilter, onEdit, onDelete }) => {
  const [sortOrder, setSortOrder] = useState("desc");

  const toggleSortOrder = () => {
    setSortOrder(sortOrder === "desc" ? "asc" : "desc");
  };

  const sortedItems = useMemo(() => {
    return items.sort((a, b) => {
      const dateA = new Date(a.trade_date);
      const dateB = new Date(b.trade_date);
      return sortOrder === "desc" ? dateB - dateA : dateA - dateB;
    });
  }, [items, sortOrder]);

  return (
    <div>
      <h1>Transactions</h1>
      <div className="mb-3 d-flex justify-content-between align-items-center">
        <div style={{ width: "80%" }}>
          {" "}
          {/* Adjust width as needed */}
          <input
            type="text"
            className="form-control"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Filter by Ticker"
          />
        </div>
        <button
          style={{ backgroundColor: "#007bff", color: "white", padding: "10px 20px" }}
          className="btn btn-outline-secondary btn-sm"
          onClick={toggleSortOrder}
        >
          {sortOrder === "desc" ? "Most recent" : "Oldest"}
        </button>
      </div>

      {items.length > 0 ? (
        <table className="table table-striped table-hover">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Sector</th>
            <th>Trade Date</th>
            <th>Transaction Type</th>
            <th>Actions</th>
            <th>Comments</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.ticker}</td>
              <td>{item.quantity}</td>
              <td>${item.price}</td>
              <td>{item.sector}</td>
              <td>{new Date(item.trade_date).toLocaleDateString()}</td>
              <td>{item.transactionType}</td>
              <td>
                <button
                  className="btn btn-primary btn-sm mx-1"
                  onClick={() => onEdit(item)}
                >
                  Edit
                </button>
                <button
                  className="btn btn-danger btn-sm mx-1"
                  onClick={() => onDelete(item.id)}
                >
                  Delete
                </button>
              </td>
              <td>{item.comments}</td>
            </tr>
          ))}
        </tbody>
      </table>      
      ) : (
        <p>No transactions to display.</p>
      )}
    </div>
  );
};

export default DisplayCryptoTransactions;
