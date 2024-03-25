import React from 'react';
import './FunctionBar.css'

function FunctionBar() {
    return (
        <div className="flex px-2 py-1 justify-content-between gap-x-2">
            <button className="flex-1 bg-green-800 text-white py-1 px-1 rounded text-xs whitespace-nowrap hover:bg-blue-700">送出我的單子</button>
            <button className="flex-1 bg-gray-300 py-1 px-1 rounded text-xs whitespace-nowrap hover:bg-blue-700">查看點單</button>
            <button className="flex-1 bg-yellow-300 py-1 px-1 rounded text-xs whitespace-nowrap hover:bg-blue-700">這個功能還沒好</button>
        </div>
    );
}

export default FunctionBar;