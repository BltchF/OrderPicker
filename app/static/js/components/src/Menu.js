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
        <div className="row py-1 ">
            <div className="col-4">
                {menu.item_name}
            </div>
            <div className="col-8 d-flex flex-nowrap align-items-between">
                <button className="btn btn-primary py-1" onClick={() => setShowPopup(true)}>調整</button>
                <QuantitySelector item_id={menu.item_id} />
                <button className="btn btn-primary py-1" onClick={orderItem}>買這個</button>
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
