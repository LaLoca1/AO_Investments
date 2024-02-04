import React, { useState } from 'react';

const NewsCard = ({ data }) => {
    return (
        <div className="news-card">
            <img src={data.imageUrl} alt={data.title} />
            <h3>{data.title}</h3>
            <p>{data.description}</p>
        </div>
    );
};

const NewsGrid = ({ news }) => {
    return (
        <div className='news-grid'>
            {news.map((newsItem, index) => (
                <NewsCard key={index} data={newsItem} />
            ))}
        </div>
    );
};

const SearchComponent = () => {
    const [query, setQuery] = useState(""); 
    const [news, setNews] = useState([]); 

    const handleSearch = () => {
        fetch(`http://localhost:8000/news/get_news/${query}`)
            .then(response => response.json()) 
            .then(data => setNews(data)); 
    }; 

    return (
        <div>
            <input type="text" value={query} onChange={e => setQuery(e.target.value)} /> 
            <button onClick={handleSearch}>Search</button>
            <NewsGrid news={news} /> 
        </div>
    );
};

export default SearchComponent;
