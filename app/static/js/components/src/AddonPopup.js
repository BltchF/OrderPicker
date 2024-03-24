import React from 'react';
import './AddonPopup.css';

function AddonPopup({ item_id, onClose }) {
    const [addons, setAddons] = React.useState([]);
    const [selectedAddons, setSelectedAddons] = React.useState([]);

    React.useEffect(() => {
        fetch(`/api/addons?item_id=${item_id}`)
            .then(response => response.json())
            .then(data => setAddons(data))
            .catch(error => console.error('Error:', error));
    }, [item_id]);

    function handleCheckboxChange(id) {
        setSelectedAddons(prevSelectedAddons =>
            prevSelectedAddons.includes(id)
                ? prevSelectedAddons.filter(addonId => addonId !== id)
                : [...prevSelectedAddons, id]
        );
    }

    function handleCheck() {
        fetch('/api/selected_addons', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_id: item_id,
                addons: selectedAddons,
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                onClose();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    return (
        <div className="popup-container">
            <ul>
                {addons.map(addon => (
                    <li key={addon.id}>
                        <input
                            type="checkbox"
                            checked={selectedAddons.includes(addon.id)}
                            onChange={() => handleCheckboxChange(addon.id)}
                        />
                        {addon.name}
                    </li>
                ))}
            </ul>
            <button className="confirm-button" onClick={handleCheck}>Check</button>
            <button className="cancel-button" onClick={onClose}>Cancel</button>
        </div>
    );
}

export default AddonPopup;