import React, {useEffect, useState} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import FunctionBar from './functionBar';
import Menu from './Menu';
// import reportWebVitals from './reportWebVitals'; 測試用
// reportWebVitals();

function MenuDisplay(){
    const [categories, setCategories] = useState([]);
    useEffect(() => {
        fetch(`/api/menus?store=${window.storeName}`)
            .then(response => response.json())
            .then(data => setCategories(data));
    }, []);
    return (
        <React.StrictMode>
            <FunctionBar/>
            {categories.map(category => (
                <div key={category.category}>
                    <h3 style={{backgroundColor: 'gray'}}>{category.category}</h3>
                    {category.items.map(menu => <Menu key={menu.item_id} menu={menu} />)}
                </div>
            ))}
        </React.StrictMode>
    );
}


ReactDOM.render(
    <MenuDisplay />,
    document.getElementById('root')
);



