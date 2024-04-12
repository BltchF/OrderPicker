/** @jsxImportSource @emotion/react */
import axios from 'axios';
import { useState, useEffect } from 'react';
import Modal from 'react-modal';
import styled from '@emotion/styled';

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

const Title = styled.div`
    font-size: 1.8rem;
    margin-bottom: 1rem;
`;

const Item = styled.div`
    font-size: 1.4rem;
    color: lightorange;
`;

const Addition = styled.div`
    font-size: 1rem;
`;

const ItemContainer = styled.div`
    margin-bottom: 1rem;
`;

const AdditionContainer = styled.div`
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
`;

const TitleContainer = styled.div`
    display: flex; 
    justify-content: space-between; 
    align-items: center;
`;

const CloseButton = styled.button`
    background-color: red;
    color: white;
    border: 1px solid white;
    border-radius: 50%;
    padding: 10px 15px;
    cursor: pointer;
    font-size: 1rem;
    &:hover {
        background-color: darkred;
    }
`;

const OrderAddition = ({ addition }) => (
    <AdditionContainer>
        <span>選項: {addition.name}</span>
        <span > $: {addition.price}</span>
    </AdditionContainer>
);

const OrderItem = ({ item }) => (
    <ItemContainer>
        <Item>{item.name}</Item>
        <span>數量: {item.quantity}</span>
        {item.additions.length > 0 && (
            <div>
                <Addition>Additions:</Addition>
                {item.additions.map((addition, index) => (
                    <OrderAddition key={index} addition={addition} />
                ))}
            </div>
        )}
    </ItemContainer>
);

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
            <TitleContainer>
                <Title>我的訂單</Title>
                <CloseButton onClick={onRequestClose}>Close</CloseButton>
            </TitleContainer>
            {order && order.items.map((item, index) => (
                <OrderItem key={index} item={item} />
            ))}
            <CloseButton onClick={onRequestClose}>Close</CloseButton>
        </Modal>
    );
}

export default MyOrderPopup;

