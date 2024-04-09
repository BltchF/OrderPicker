/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import Modal from 'react-modal';

const customStyles = {
    content: {
        top: '50%',
        maxHeight: '90vh',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
        background: 'black',
        borderRadius: '4px',
        padding: '20px',
        color: '#ffffff',
        overflow: 'auto'
    },
    overlay: {
        backgroundColor: '#181818'
    }
};

const user_id = window.user_id;

//-----style start-----
const titleStyle = css`fontSize: 1.8rem;`;
const itemStyle = css`fontSize: 1.4rem; color: lightorange;`;
const additionStyle = css`fontSize: 1rem;`;
const itemContainerStyle = css`marginBottom: 1rem;`;
const additionContainerStyle = css`
    marginBottom: 0.5rem;
    display: flex;
    justifyContent: space-between;
`;
const titleContainer = css`
    display: flex; 
    justifyContent: space-between; 
    alignItems: center;
`;
//-----style end-----

function MyOrderPopup({ isOpen, onRequestClose }) {
    const [order, setOrder] = useState(null);

    useEffect(() => {
        if (isOpen) {
            axios.get('/api/order', { params: { user_id: user_id } })
                .then(response => {
                    setOrder(response.data);
                })
                .catch(error => {
                    console.error('Error fetching order:', error);
                });
        }
    }, [isOpen]);

    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            style={customStyles}
            contentLabel="我的訂單"
        >
            <div css={titleContainer}>
                <div css={titleStyle}>我的訂單</div>
                <button onClick={onRequestClose}>Close</button>
            </div>
            {order && order.items.map((item, index) => (
                <div key={index} css={itemContainerStyle}>
                    <div css={itemStyle}>{item.name}</div>
                    <p>Quantity: {item.quantity}</p>
                    {item.additions.length > 0 && (
                        <div>
                            <div css={additionStyle}>Additions:</div>
                            {item.additions.map((addition, index) => (
                                <div key={index} css={additionContainerStyle}>
                                    <p>Name: {addition.name}</p>
                                    <p>Price: {addition.price}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            ))}
            <button onClick={onRequestClose}>Close</button>
        </Modal>
    );
}

export default MyOrderPopup;