import React, { useEffect } from 'react';
import QuantitySelector from './QuantitySelector';
import AddonPopup from './AddonPopup';
import "./Menu.css";
import Modal from 'react-modal';


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
        <div className="flex flex-row py-1 min-w-200">
            <div className="w-1/3">
                {menu.item_name}
            </div>
            <div className="w-2/3 flex flex-nowrap justify-between">
                <button className="rounded-md bg-blue-500 py-1 px-1 flex-nowrap" onClick={() => setShowPopup(true)}>調整</button>
                <QuantitySelector item_id={menu.item_id} />
                <button className="rounded-md bg-blue-500 py-1 px-1 flex-nowrap" onClick={orderItem}>買這個</button>
                <Modal 
                    isOpen={showPopup}
                    onRequestClose={() => setShowPopup(false)}
                    contentLabel="Addon Popup"
                >
                    <AddonPopup item_id={menu.item_id} onClose={() => setShowPopup(false)} />
                </Modal>
            </div>
        </div>
    );
}

export default Menu;
