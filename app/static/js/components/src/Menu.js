import React, { useEffect } from 'react';
import QuantitySelector from './QuantitySelector';
import AddonPopup from './AddonPopup';
import "./Menu.css";


function Menu({ menu }) {
    const [showPopup, setShowPopup] = React.useState(false);

    const orderItem = () => {
        // ! Replace API call
        fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_id: menu.item_id,
            }),
        });
    };

    return (
        <div className="row align-items-center mm">
            <div className="col-4">
                {menu.item_name}
            </div>
            <div className="col-8 no-wrap reduced-line-height d-flex flex-nowrap">
                <button className="btn btn-primary" onClick={() => setShowPopup(true)}>調整</button>
                <QuantitySelector item_id={menu.item_id} />
                <button className="btn btn-primary" onClick={orderItem}>買這個</button>
                {showPopup && <AddonPopup item_id={menu.item_id} onClose={() => setShowPopup(false)} />}
            </div>
        </div>
    );
}

export default Menu;
