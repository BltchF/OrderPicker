import React from 'react';
import './AddonsPopup.css'; // We'll create this file next

const AddonsPopup = () => {
    return (
        <div className="popup-container">
            <h2>Select Add-ons</h2>
            {/* Add-on selection options will go here */}
            <button className="confirm-button">Confirm</button>
        </div>
    );
};

export default AddonsPopup;
