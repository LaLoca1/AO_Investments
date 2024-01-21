import React from 'react';

const DisplayTransaction = ({ items, filter, setFilter, onEdit, onDelete }) => {
  return (
    <div>
      <h1>Transactions</h1>
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter by Ticker"
        />
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
              <th>Comments</th>
              <th>Market</th>
              <th>Transaction Type</th>
              <th>Actions</th>
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
                <td>{item.comments}</td>
                <td>{item.market}</td>
                <td>{item.transactionType}</td>
                <td>
                  <button className="btn btn-primary btn-sm mx-1" onClick={() => onEdit(item)}>Edit</button>
                  <button className="btn btn-danger btn-sm mx-1" onClick={() => onDelete(item.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No watchlist items to display.</p>
      )}
    </div>
  );
};

export default DisplayTransaction;
