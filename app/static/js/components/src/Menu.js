import React, { useEffect } from 'react';
import QuantitySelector from './QuantitySelector';
import AddonPopup from './AddonPopup';
import "./Menu.css";
import Modal from 'react-modal';

function Menu({ menu, store_id }) {  
    const [showPopup, setShowPopup] = React.useState(false);
    const [setSelectedAddons] = React.useState([]);
    const user_id = window.user_id;
    const [quantity, setQuantity] = React.useState(1);

    const handleAddAddon = (addon) => {
        setSelectedAddons(prevAddons => [...prevAddons, addon]);
    };

    const orderItem = () => {
        const selectedAddons = JSON.parse(localStorage.getItem('selectedAddons')) || [];

        const items = [{
            item_id: menu.item_id,
            quantity: quantity,
            additions: selectedAddons.map(addon => addon.id),
        }];

        fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                store_id: store_id,
                user_id: user_id,
                items: items,
            }),
        });

        localStorage.removeItem('selectedAddons');
    };

    return (
        <div className="flex flex-row py-1 min-w-200">
            <div className="w-1/3">
                {menu.item_name}
            </div>
            <div className="w-2/3 flex flex-nowrap justify-between">
                <button className="rounded-md bg-blue-500 py-1 px-1 flex-nowrap" onClick={() => setShowPopup(true)}>調整</button>
                <QuantitySelector item_id={menu.item_id} 
                                quantity={quantity}
                                setQuantity={setQuantity}/>
                <button className="rounded-md bg-blue-500 py-1 px-1 flex-nowrap" onClick={orderItem}>買這個</button>
                <Modal 
                    isOpen={showPopup}
                    onRequestClose={() => setShowPopup(false)}
                    contentLabel="Addon Popup"
                >
                    <AddonPopup item_id={menu.item_id} onAddAddon={handleAddAddon} onClose={() => setShowPopup(false)} />
                </Modal>
            </div>
        </div>
    );
}

export default Menu;
