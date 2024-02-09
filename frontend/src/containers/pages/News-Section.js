// In your React component
import React, { useState } from 'react';
import './News-Section.css'

const NewsItem = ({ article }) => {
    return (
        <div className="news-item">
            <img src={article.banner_image} alt={article.title} />
            <h3>{article.title}</h3>
            <p>{article.summary}</p>
            <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
        </div>
    );
};

const NewsGrid = ({ news }) => {
    return (
        <div className="news-grid">
            {news.map((article, index) => (
                <NewsItem key={index} article={article} />
            ))}
        </div>
    );
};

const StockNews = () => {
    const [ticker, setTicker] = useState('');
    const [topic, setTopic] = useState('');
    const [news, setNews] = useState([]);

    const fetchNews = () => {
        fetch(`http://localhost:8000/news/api/get_stock_news/${ticker}/`)
            .then(response => response.json())
            .then(data => {
                setNews(data.feed || []); // Assuming 'feed' contains your news data
            })
            .catch(error => console.error('Error fetching news:', error));
    };

    const fetchTopics = () => {
        fetch(`http://localhost:8000/news/api/get_topic_news/${topic}/`)
            .then(response => response.json())
            .then(data => {
                setNews(data.feed || []); // Assuming 'feed' contains your news data
            })
            .catch(error => console.error('Error fetching news:', error));
    };

    return (
        <div className="search-container">
            <div className="search-bar">
                <div className="search-field">
                    <input 
                        type="text" 
                        value={ticker} 
                        onChange={(e) => setTicker(e.target.value)} 
                        placeholder="Enter Stock/Crypto Ticker" 
                    />
                    <button onClick={fetchNews}>Get Ticker News</button>
                </div>
                <div className="search-field">
                    <input 
                        type="text" 
                        value={topic} 
                        onChange={(e) => setTopic(e.target.value)} 
                        placeholder="Enter Topic" 
                    />
                    <button onClick={fetchTopics}>Get Topic News</button>
                </div>
            </div>
            <div className="container large-gap">
                <NewsGrid news={news} />
            </div>
        </div>
    );    
};

export default StockNews;
