const DisplayWatchlist = ({ items, onEdit, onDelete }) => {
  return (
    <div>
      <h1>Watchlist Items</h1>
      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              {item.ticker} - {item.quantity} - {item.price} - {item.sector}
              - {new Date(item.trade_date).toLocaleDateString()} - {item.comments}
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

export default DisplayWatchlist;
