const DisplayTransaction = ({ items, filter, setFilter, onEdit, onDelete }) => {
  return (
    <div>
      <h1>Watchlist Items</h1>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter by Ticker"
        />
      </div>

      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              {item.ticker} - {item.quantity} - {item.price} - {item.sector}-{" "}
              {new Date(item.trade_date).toLocaleDateString()} - {item.comments} - {item.market}
              - {item.transactionType}
              <button onClick={() => onEdit(item)}>Edit</button>
              <button onClick={() => onDelete(item.id)}>Delete</button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No watchlist items to display.</p>
      )}
    </div>
  );
};

export default DisplayTransaction;
