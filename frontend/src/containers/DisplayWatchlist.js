import React, { useEffect, useState } from 'react'; 
import axios from 'axios';


const DisplayWatchlist = () => {
    const [watchlistItems, setWatchlistItems] = useState([]);
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await axios.get('/watchlist/api/user/watchlist-items');
          setWatchlistItems(response.data);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };
  
      fetchData();
    }, []);

    return (
        <div>
          <h1>Watchlist Items</h1>
          <ul>
            {watchlistItems.map(item => (
              <li key={item.id}>{item.ticker} - {item.quantity} - {item.price}</li>
            ))}
          </ul>
        </div>
      );
    };
    
export default DisplayWatchlist; 