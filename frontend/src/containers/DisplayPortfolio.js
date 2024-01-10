import React, { useEffect, useState } from "react";
import axios from "axios";

const DisplayPortfolio = () => {
  const [portfolio, setPortfolio] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/watchlist/api/user/transaction-items");
      setPortfolio(calculatePortfolio(response.data));
    } catch (error) {
      console.error("Error fetching portfolio data:", error);
    } finally {
      setLoading(false);
    }
  };

  const calculatePortfolio = (transactions) => {
    const portfolio = {};
    transactions.forEach(({ ticker, quantity, price, transactionType }) => {
      if (!portfolio[ticker]) {
        portfolio[ticker] = { totalQuantity: 0, totalCost: 0 };
      }
      if (transactionType === "buy") {
        portfolio[ticker].totalQuantity += quantity;
        portfolio[ticker].totalCost += quantity * price;
      } else if (transactionType === "sell") {
        portfolio[ticker].totalQuantity -= quantity;
      }
    });

    for (const ticker in portfolio) {
      const stock = portfolio[ticker];
      stock.averagePrice =
        stock.totalQuantity > 0 ? stock.totalCost / stock.totalQuantity : 0;
    }
    return portfolio;
  };

  return (
    <div>
      <h1>User Portfolio</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Total Quantity</th>
              <th>Average Price</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(portfolio).map(
              ([ticker, { totalQuantity, averagePrice }]) => (
                <tr key={ticker}>
                  <td>{ticker}</td>
                  <td>{totalQuantity}</td>
                  <td>${averagePrice.toFixed(2)}</td>
                </tr>
              )
            )}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default DisplayPortfolio;
