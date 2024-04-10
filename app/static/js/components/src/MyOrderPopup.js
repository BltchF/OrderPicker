/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import Modal from 'react-modal';

const user_id = window.user_id;

const customStyles = {
        content: {
            top: '50%',
            left: '50%',
            maxHeight: '90vh',
            right: 'auto',
            bottom: 'auto',
            marginRight: '10vw',
            marginLeft: '10vw',
            transform: 'translate(-50%, -50%)',
            background: 'black',
            borderRadius: '4px',
            padding: '20px',
            color: '#ffffff',
            overflow: 'auto'
        },
        overlay: {
            backgroundColor: 'rgba(112, 160, 255, 0.5)',
            backdropFilter: 'blur(5px)',
        }
    };
const titleStyle = css`
    fontSize: 1.8rem;
    marginBottom: 1rem;`;
const itemStyle = css`
    fontSize: 1.4rem; color: lightorange;
    `;
const additionStyle = css`
    fontSize: 1rem;
    `;
const itemContainerStyle = css`
    marginBottom: 1rem;
    `;
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
                    <span>數量: {item.quantity}</span>
                    {item.additions.length > 0 && (
                        <div>
                            <div css={additionStyle}>Additions:</div>
                            {item.additions.map((addition, index) => (
                                <div key={index} css={additionContainerStyle}>
                                    <span>選項: {addition.name}</span>
                                    <span > $: {addition.price}</span>
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