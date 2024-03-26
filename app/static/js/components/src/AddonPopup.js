import React from 'react';
import './AddonPopup.css';

function AddonPopup({ item_id, onClose }) {
    const [addons, setAddons] = React.useState([]);
    const [selectedAddons, setSelectedAddons] = React.useState([]);
    
    // ! TODO: Fetch addons
    React.useEffect(() => {
    fetch(`/api/addons?item_id=${item_id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setAddons(data);
        })
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
    <div className="fixed z-10 inset-0 overflow-y-auto flex items-center justify-center">
        <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
                <div className="absolute inset-0 bg-gray-500"></div>
            </div>

            <div className="inline-block align-middle bg-white rounded-lg 
            text-left overflow-hidden shadow-xl transform transition-all 
            sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 z-10">
                    <ul>
                        {addons.map(addon => (
                            <li key={addon.id} className="flex items-center justify-between p-2">
                                <span className="text-gray-700">{addon.add_name}</span>
                                <input
                                    type="checkbox"
                                    checked={selectedAddons.includes(addon.id)}
                                    onChange={() => handleCheckboxChange(addon.id)}
                                    className="form-checkbox h-5 w-5 text-blue-600"
                                />
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse z-10">
                    <button type="button" className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm" onClick={handleCheck}>
                        Check
                    </button>
                    <button type="button" className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:w-auto sm:text-sm" onClick={onClose}>
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
);
}

export default AddonPopup;