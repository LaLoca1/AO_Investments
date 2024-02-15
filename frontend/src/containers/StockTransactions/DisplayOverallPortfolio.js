import React, { useEffect, useState } from "react";
import axios from "axios";
import "./DisplayPortfolio.css";

const DisplayOverallPortfolio = () => {
  const [overallPortfolio, setOverallPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);

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

  return (
    <div className="overall-table-container">
      {loading ? (
        <p>Loading...</p>
      ) : overallPortfolio ? (
        <div className="overall-performance-container">
          <h3>Overall Stock Portfolio Performance</h3>
          <table className="table table-striped table-hover">
            <tbody>
              <tr>
                <th>Total Investment</th>
                <td>${overallPortfolio.totalPortfolioInvestment?.toFixed(2)}</td>
              </tr>
              <tr>
                <th>Total Value</th>
                <td>${overallPortfolio.totalPortfolioValue?.toFixed(2)}</td>
              </tr>
              <tr>
                <th>Total Profit or Loss</th>
                <td
                  className={
                    overallPortfolio.totalPortfolioProfitOrLoss >= 0
                      ? "text-success"
                      : "text-danger"
                  }
                >
                  ${overallPortfolio.totalPortfolioProfitOrLoss?.toFixed(2)}
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

export default DisplayOverallPortfolio;
