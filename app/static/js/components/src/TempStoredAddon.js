/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

const addonStyle = css`
    border: 1px solid black;
    margin: 10px;
    padding: 10px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
`;

function TempStoreAddon({ selectedAddons }) {
    const flatSelectedAddons = selectedAddons.flat();


    return (
        <div>
            {flatSelectedAddons.map((addon) => (
                <div key={addon.id} css={addonStyle}>
                    <span>[+]:{addon.add_name}</span>
                    <span>/$: {addon.add_price}</span>
                </div>
            ))}
        </div>
    );
}

export default TempStoreAddon;