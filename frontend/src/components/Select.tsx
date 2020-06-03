import React from "react";

interface Props {
    defaultOption?: Option;
    options: Option[];
    onChange?: Function;
}

export interface Option {
    value: string; 
    text: string;
}

export default function({ defaultOption, options, onChange }: Props) {
    if (!defaultOption) 
        defaultOption = {
            text: "Select",
            value: "",
        };

    return (
        <div className="select">
            <select onChange={(e) => onChange ? onChange(e.target.value) : null}>
                <option value={defaultOption.value}>{defaultOption.text}</option>
                {options.map((option) => (
                    <option key={option.value} value={option.value}>{option.text}</option>
                ))}
            </select>
        </div>
    );
}