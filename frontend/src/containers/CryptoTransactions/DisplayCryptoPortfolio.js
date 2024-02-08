import React, { useEffect, useState } from "react";
import axios from "axios";
import "./DisplayPortfolio.css";

const DisplayCryptoPortfolio = () => {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/crypto-transactions/api/user/crypto-portfolio/");
      setPortfolio(response.data);
    } catch (error) {
      console.error("Error fetching portfolio data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="table-container">
      <h2 className="sticky-title">Crypto Portfolio Overview</h2>
      <div className="table-container">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="table table-striped table-hover">
            <thead className="thead-dark">
              <tr>
                <th>Coin</th>
                <th>Total Quantity</th>
                <th>Average Price</th>
                <th>Total Investment</th>
                <th>Current Value</th>
                <th>Net Gain/Loss</th>
                <th>Percentage Gain/Loss</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.map(
                ({
                  coin,
                  totalQuantity,
                  averagePrice,
                  totalInvestment,
                  currentValue,
                  profitOrLoss,
                }) => {
                  const percentageChange =
                    ((currentValue - totalInvestment) / totalInvestment) * 100;
                  return (
                    <tr key={coin}>
                      <td>{coin}</td>
                      <td>{totalQuantity}</td>
                      <td>${averagePrice.toFixed(2)}</td>
                      <td>${totalInvestment.toFixed(2)}</td>
                      <td>${currentValue.toFixed(2)}</td>
                      <td
                        className={
                          profitOrLoss >= 0 ? "text-success" : "text-danger"
                        }
                      >
                        ${profitOrLoss.toFixed(2)}
                      </td>
                      <td
                        className={
                          percentageChange >= 0 ? "text-success" : "text-danger"
                        }
                      >
                        {percentageChange.toFixed(2)}%
                      </td>
                    </tr>
                  );
                }
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default DisplayCryptoPortfolio;
