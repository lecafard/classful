import React from "react";

interface Props {
  label: string;
  type: string;
  value?: string;
  placeholder?: string;
  onChange?: Function;
  required?: boolean;
}


export default function Input({label, type, value, placeholder, onChange, required}: Props) {
  return (
    <div className="field is-horizontal">
      <div className="field-label is-normal">
        <label className="label">{label}</label>
      </div>
      <div className="field-body">
        <div className="field">
          <p className="control">
            <input
              className="input"
              type={type}
              onChange={(e) => onChange ? onChange(e.target.value) : null}
              placeholder={placeholder}
              value={value}
              required={required}
            />
          </p>
        </div>
      </div>
    </div>
  )
}