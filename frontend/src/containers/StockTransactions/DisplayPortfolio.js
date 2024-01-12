import React, { useEffect, useState } from "react";
import axios from "axios";

const DisplayPortfolio = () => {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/watchlist/api/user/portfolio/");
      setPortfolio(response.data);  // Assuming this is already aggregated data
    } catch (error) {
      console.error("Error fetching portfolio data:", error);
    } finally {
      setLoading(false);
    }
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
            {portfolio.map(({ ticker, totalQuantity, averagePrice }) => (
              <tr key={ticker}>
                <td>{ticker}</td>
                <td>{totalQuantity}</td>
                <td>${averagePrice.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default DisplayPortfolio;
