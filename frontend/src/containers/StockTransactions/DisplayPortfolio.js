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
      setPortfolio(response.data); // Assuming this is already aggregated data
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
              <th>Total Investment</th>
              <th>Current Value</th>
              <th>Profit/Loss</th>
            </tr>
          </thead>
          <tbody>
            {portfolio.map(
              ({
                ticker,
                totalQuantity,
                averagePrice,
                totalInvestment,
                currentValue,
                profitOrLoss,
              }) => (
                <tr key={ticker}>
                  <td>{ticker}</td>
                  <td>{totalQuantity}</td>
                  <td>${averagePrice.toFixed(2)}</td>
                  <td>${totalInvestment.toFixed(2)}</td>
                  <td>${currentValue.toFixed(2)}</td>
                  <td className={profitOrLoss >= 0 ? "profit" : "loss"}>
                    ${profitOrLoss.toFixed(2)}
                  </td>
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
