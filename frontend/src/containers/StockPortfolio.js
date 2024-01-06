import React, {useState, useEffect } from 'react'; 
import axios from 'axios'; 
import DisplayWatchlist from './DisplayWatchlist';
import AddWatchlistItem from './AddWatchlistItem';
import EditWatchlistItem from './EditWatchlistItem';
import DisplayPortfolio from './DisplayPortfolio';

const StockPortfolio = () => {
    const [watchlistItems, setWatchlistItems] = useState([]);
    const [editingItem, setEditingItem] = useState(null); 
    const [showAddForm, setShowAddForm] = useState(false); 

    // Fetch watchlist items on component mount 
    useEffect(() => {
        fetchWatchlistItems(); 
    }, []); 

    const fetchWatchlistItems = async () => {
        try {
            const response = await axios.get('/watchlist/api/user/watchlist-items'); 
            setWatchlistItems(response.data); 
        } catch (error) {
            console.error('Error fetching watchlist items:', error); 
        }
    };

    const handleAddItem = async (newItem) => {
        setShowAddForm(false); 
    }; 

    const handleEdit = (item) => {
        setEditingItem(item); 
    };

    const handleSaveEdit = async (editedItem) => {
        // Logic to save the edited item to your backend and update the list 
    };

    const handleCancelEdit = () => {
        setEditingItem(null); 
    }; 

    return (
        <div>
            <DisplayPortfolio /> 
            <AddWatchlistItem onItemAdded={handleAddItem} />
            <DisplayWatchlist items={watchlistItems} onEdit={handleEdit} /> 
            {editingItem && (
                <EditWatchlistItem
                    item={editingItem}
                    onSave={handleSaveEdit} 
                    onCancel={handleCancelEdit}
                    />
            )}
        </div>
    );
}; 

export default StockPortfolio; 