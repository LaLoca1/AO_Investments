import React, { useEffect, useState } from "react";
import axios from "axios";
import "./DisplayPortfolio.css";

const DisplayCombinedOverallPortfolio = () => {
  const [overallPortfolio, setOverallPortfolio] = useState(null);
  const [overallCryptoPortfolio, setOverallCryptoPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchOverallCryptoPortfolioData();
  }, []);

  const fetchOverallCryptoPortfolioData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        "/crypto-transactions/api/user/crypto-portfolio/"
      );
      console.log("API Response:", response.data);
      if (response.data && response.data.overallCryptoPortfolio) {
        console.log(
          "Setting Overall Portfolio:",
          response.data.overallCryptoPortfolio
        );
        setOverallCryptoPortfolio(response.data.overallCryptoPortfolio);
      }
    } catch (error) {
      console.error("Error fetching overall portfolio data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverallPortfolioData();
  }, []);

  const fetchOverallPortfolioData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/watchlist/api/user/portfolio/");
      if (response.data && response.data.overallPortfolio) {
        setOverallPortfolio(response.data.overallPortfolio);
      }
    } catch (error) {
      console.error("Error fetching overall portfolio data:", error);
    } finally {
      setLoading(false);
    }
  };

  const sumAndFormat = (value1, value2) => {
    const sum = (value1 ?? 0) + (value2 ?? 0); // Handle null or undefined
    return sum.toFixed(2); // Format to 2 decimal places
  };

  return (
    <div className="overall-table-container">
      {loading ? (
        <p>Loading...</p>
      ) : overallPortfolio && overallCryptoPortfolio ? (
        <div className="overall-performance-container">
          <h3>Overall Portfolio Performance</h3>
          <table className="table table-striped table-hover">
            <tbody>
              <tr>
                <th>Total Investment</th>
                <td>
                  $
                  {sumAndFormat(
                    overallPortfolio.totalPortfolioInvestment,
                    overallCryptoPortfolio.totalCryptoPortfolioInvestment
                  )}
                </td>
              </tr>
              <tr>
                <th>Total Value</th>
                <td>
                  $
                  {sumAndFormat(
                    overallPortfolio.totalPortfolioValue,
                    overallCryptoPortfolio.totalCryptoPortfolioValue
                  )}
                </td>
              </tr>
              <tr>
                <th>Total Profit or Loss</th>
                <td
                  className={
                    overallPortfolio.totalPortfolioProfitOrLoss +
                      overallCryptoPortfolio.totalCryptoPortfolioProfitOrLoss >=
                    0
                      ? "text-success"
                      : "text-danger"
                  }
                >
                  $
                  {sumAndFormat(
                    overallPortfolio.totalPortfolioProfitOrLoss,
                    overallCryptoPortfolio.totalCryptoPortfolioProfitOrLoss
                  )}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <p>No data available</p>
      )}
    </div>
  );
};

export default DisplayCombinedOverallPortfolio;
