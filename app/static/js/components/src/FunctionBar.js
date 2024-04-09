import React, { useState } from 'react';
import './FunctionBar.css'
import MyOrderPopup from './MyOrderPopup';

function FunctionBar() {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    return (
        <div className="flex px-2 py-1 justify-content-between gap-x-2">
            <button className="flex-1 bg-green-800 text-white py-1 px-1 rounded text-xs whitespace-nowrap hover:bg-blue-700">跟單</button>
            <button onClick={handleOpenModal} className="flex-1 bg-gray-900 py-1 px-1 rounded text-xs whitespace-nowrap hover:bg-blue-700">查看我的點單</button>
            <button className="flex-1 bg-yellow-500 py-1 px-1 rounded text-xs whitespace-nowrap hover:bg-blue-700">查看全部點單</button>
            <MyOrderPopup isOpen={isModalOpen} onRequestClose={handleCloseModal} />
        </div>
    );
}

export default FunctionBar;