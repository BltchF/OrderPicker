import React from 'react';
import QuantitySelector from './QuantitySelector';

function Menu({ menu }) {
    return (
        <div style={{display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center'
        }}>
            {menu.item_name}
            <QuantitySelector item_id={menu.item_id} />
        </div>
    );
}

export default Menu;