import React from "react";
import "./QuantitySelector.css";

class QuantitySelector extends React.Component {
    render() {
        const { quantity, setQuantity } = this.props;

        const increaseQuantity = () => {
            setQuantity(quantity + 1);
        }

        const decreaseQuantity = () => {
            if (quantity > 0) {
                setQuantity(quantity - 1);
            }
        }

        return (
            <div className="input-group quantity-selector d-flex align-items-between flex-nowrap">
                <div className="input-group-prepend">
                    <button className="btn btn-outline-secondary" type="button"
                        onClick={decreaseQuantity}>-</button>
                </div>
                <input type="text" id={`quantity-${this.props.item_id}`} className="form-control-sm" value={quantity} readOnly />
                <div className="input-group-append">
                    <button className="btn btn-outline-secondary" type="button"
                        onClick={increaseQuantity}>+</button>
                </div>
            </div>
        );
    }
}

export default QuantitySelector;