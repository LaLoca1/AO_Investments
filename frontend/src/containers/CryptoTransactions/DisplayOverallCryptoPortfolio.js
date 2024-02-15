import React, { useEffect, useState } from "react";
import axios from "axios";
import "./DisplayPortfolio.css";

const DisplayOverallCryptoPortfolio = () => {
  const [overallCryptoPortfolio, setOverallCryptoPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchOverallCryptoPortfolioData();
  }, []);

  const fetchOverallCryptoPortfolioData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/crypto-transactions/api/user/crypto-portfolio/");
      console.log("API Response:", response.data);
      if (response.data && response.data.overallCryptoPortfolio) {
        console.log("Setting Overall Portfolio:", response.data.overallCryptoPortfolio);
        setOverallCryptoPortfolio(response.data.overallCryptoPortfolio);
      }
    } catch (error) {
      console.error("Error fetching overall portfolio data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="overall-table-container">
      {loading ? (
        <p>Loading...</p>
      ) : overallCryptoPortfolio ? (
        <div className="overall-performance-container">
          <h3>Overall Crypto Portfolio Performance</h3>
          <table className="table table-striped table-hover">
            <tbody>
              <tr>
                <th>Total Investment</th>
                <td>${overallCryptoPortfolio.totalCryptoPortfolioInvestment?.toFixed(2)}</td>
              </tr>
              <tr>
                <th>Total Value</th>
                <td>${overallCryptoPortfolio.totalCryptoPortfolioValue?.toFixed(2)}</td>
              </tr>
              <tr>
                <th>Total Profit or Loss</th>
                <td
                  className={
                    overallCryptoPortfolio.totalCryptoPortfolioProfitOrLoss >= 0
                      ? "text-success"
                      : "text-danger"
                  }
                >
                  ${overallCryptoPortfolio.totalCryptoPortfolioProfitOrLoss?.toFixed(2)}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default DisplayOverallCryptoPortfolio;
