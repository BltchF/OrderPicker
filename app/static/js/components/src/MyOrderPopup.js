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
        width: '90vw',
        right: 'auto',
        bottom: 'auto',
        transform: 'translate(-50%, -50%)',
        background: 'rgba(1, 12, 26, 0.77)',
        borderRadius: '4px',
        padding: '1rem',
        color: '#ffffff',
        overflow: 'auto'
    },
    overlay: {
        backgroundColor: 'rgba(21, 48, 101, 0.63)',
        backdropFilter: 'blur(5px)',
    }
};

const Title = styled.div`
    font-size: 1.3rem;
    margin-bottom: 1rem;
`;

const Item = styled.span`
    color: lightorange;
`;



const ItemContainer = styled.div`
    margin-bottom: 1rem;
`;

const AdditionContainer = styled.div`
    jdisplay: flex;
    font-size: 0.8rem;
    color: rgb(114, 180, 255);
    justify-content: space-between;
`;

const TitleContainer = styled.div`
    display: flex; 
    justify-content: space-between; 
    align-items: center;
`;

const CloseButton = styled.button`
    background-color: rgba(237, 50, 50, 0.3);
    color: white;
    border: 1px solid white;
    border-radius: 0.3rem;
    padding: 0.1rem 0.6rem;
    cursor: pointer;
    font-size: 1rem;
    &:hover {
        background-color: rgba(67, 0, 0, 0.58);
    }
`;

const DeleteItemButton = styled.button`
    background-color: rgba(237, 50, 50, 0.3);
    color: white;
    border: 1px solid white;
    border-radius: 0.3rem;
    padding: 0.1rem 0.6rem;
    cursor: pointer;
    font-size: 0.7rem;
`;

const OrderAddition = ({ addition }) => (
    <AdditionContainer>
        <span>選項: {addition.name}</span>
        <span > +$ {addition.price}</span>
    </AdditionContainer>
);

const OrderItem = ({ item, handleDelete }) => (
    <ItemContainer>
        <div style={{display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid white'}}>
            <div>
            <Item>{item.name} </Item>
            <span>x {item.quantity}</span>
            </div>
            <DeleteItemButton onClick={() => handleDelete(item.id)}>刪除</DeleteItemButton>
        </div>
        {item.additions.length > 0 && (
            <div>
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

    const handleDelete = (itemId) => {
    axios.delete(`/api/order/${itemId}`)
        .then(() => {
            setOrder(prevOrder => ({
                ...prevOrder,
                items: prevOrder.items.filter(item => item.id !== itemId)
            }));
        })
        .catch(error => {
            console.error('Error deleting item:', error);
        });
    };

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
                <div key={index}>
                    <OrderItem item={item} handleDelete={handleDelete}/>

                </div>
            ))}
            <CloseButton onClick={onRequestClose}>Close</CloseButton>
        </Modal>
    );
}

export default MyOrderPopup;

