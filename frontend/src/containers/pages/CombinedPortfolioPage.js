import React from 'react';
import DisplayOverallCryptoPortfolio from "../CryptoTransactions/DisplayOverallCryptoPortfolio";
import DisplayOverallPortfolio from "../StockTransactions/DisplayOverallPortfolio";
import DisplayCombinedOverallPortfolio from "../StockTransactions/DisplayCombinedOverallPortfolio";
import './ParentComponent.css'; // Your stylesheet for layout

const CombinedPortfolioPage = () => {
  return (
    <div className="portfolio-page-container">
      <h1 className="portfolio-page-title">My Investment Portfolio</h1>
      <section className="portfolio-section">
        <DisplayOverallPortfolio />
      </section>
      <section className="portfolio-section">
        <DisplayOverallCryptoPortfolio />
      </section>
      <section className="portfolio-section">
        <DisplayCombinedOverallPortfolio />
      </section>
    </div>
  );
};

export default CombinedPortfolioPage;
