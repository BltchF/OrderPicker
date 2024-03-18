import React, {useEffect, useState} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import Menu from './Menu';

function App(){
    const [categories, setCategories] = useState([]);
    useEffect(() => {
        fetch(`/api/menus?store=${window.storeName}`)
            .then(response => response.json())
            .then(data => setCategories(data));
    }, []);
    return (
        <React.StrictMode>
            {categories.map(category => (
                <div key={category.category}>
                    <h2>{category.category}</h2>
                    {category.items.map(menu => <Menu key={menu.item_id} menu={menu} />)}
                </div>
            ))}
        </React.StrictMode>
    );
}


ReactDOM.render(
  <App />,
  document.getElementById('root')
);

reportWebVitals();

