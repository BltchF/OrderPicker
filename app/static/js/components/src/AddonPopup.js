import React from 'react';
import Modal from 'react-modal';
import styled from "@emotion/styled";

const modalStyles = {
    content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
        padding: '1rem',
        backgroundColor: 'rgb(19, 18, 29)',
        borderRadius: '0.375rem',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        border: 'none',
        width: '90wv',
    },
    overlay: {
        backgroundColor: 'rgba(2, 27, 55, 0.5)',
        backdropFilter: 'blur(5px)',
    },
};

const StyledContainer = styled.div`
    backgraound-color: rgb(14, 36, 63);
    content-align: center;
`;

const StyledDiv = styled.div`
    text-align: left;
    padding: 2rem;
`;

const StyledInput = styled.input`
    padding-left: 2rem;
`;
const ButtonContainer = styled.div`
    display: flex;
    justify-content: space-around;
`;

const StyledButton = styled.button`
    &:first-of-type {
        background-color: blue;
        border: 1px solid white;
        color: white;
        margin-right: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    &:last-of-type {
        background-color: gray;
        border: 1px solid white;
        color: white;
        padding-left: 1rem;
        padding-right: 1rem;
    }
`;



function AddonPopup({ item_id, onAddAddon, isOpen, onClose }) {
    const [addons, setAddons] = React.useState([]);
    const [selectedAddons, setSelectedAddons] = React.useState([]);
    
    React.useEffect(() => {
    fetch(`/api/addons?item_id=${item_id}`)
        .then(response => response.json())
        .then(data => {
            setAddons(data);
        })
        .catch(error => console.error('Error:', error));
        }, [item_id]);

    function handleCheckboxChange(id) {
    const addon = addons.find(addon => addon.id === id);
    setSelectedAddons(selectedAddons =>
        selectedAddons.some(selectedAddon => selectedAddon.id === id)
            ? selectedAddons.filter(selectedAddon => selectedAddon.id !== id)
            : [...selectedAddons, addon]
        );
    }

    function handleCheck() {
        onAddAddon(selectedAddons);
        localStorage.setItem('selectedAddons', JSON.stringify(selectedAddons));
        onClose();
        }

    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onClose}
            contentLabel="Addon Popup"
            style={modalStyles}
        >
            <StyledContainer>
                <div>
                    {addons.map(addon => (
                        <StyledDiv key={addon.id}>
                            <span>{addon.add_name}</span>
                            <StyledInput
                                type="checkbox"
                                checked={selectedAddons.some(selectedAddons => selectedAddons.id === addon.id)}
                                onChange={() => handleCheckboxChange(addon.id)}
                            />
                        </StyledDiv>
                    ))}
                </div>
            </StyledContainer>
            <ButtonContainer>
            <StyledButton type="button" onClick={handleCheck}>
                Check
            </StyledButton>
            <StyledButton type="button" onClick={onClose}>
                Cancel
            </StyledButton>
            </ButtonContainer>
        </Modal>
    );
}

export default AddonPopup;