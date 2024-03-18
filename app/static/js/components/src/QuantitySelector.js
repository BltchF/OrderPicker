import React from "react";


class QuantitySelector extends React.Component {
    constructor(props) {
        super(props);
        this.state = { quantity: 0 };
    }

    increaseQuantity = () => {
        this.setState({ quantity: this.state.quantity + 1 });
    }

    decreaseQuantity = () => {
        if (this.state.quantity > 0) {
            this.setState({ quantity: this.state.quantity - 1 });
        }
    }

    render() {
        return (
            <div className="input-group ml-2">
                <div className="input-group-prepend">
                    <button className="btn btn-outline-secondary" type="button"
                        onClick={this.decreaseQuantity}>-</button>
                </div>
                <input type="text" id={`quantity-${this.props.item_id}`} className="form-control" value={this.state.quantity} readOnly />
                <div className="input-group-append">
                    <button className="btn btn-outline-secondary" type="button"
                        onClick={this.increaseQuantity}>+</button>
                </div>
            </div>
        );
    }
}

export default QuantitySelector;
