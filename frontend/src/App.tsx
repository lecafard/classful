import React, { useState, useEffect } from 'react';
import './App.scss';
import Select from './components/Select';
import { getTerms } from './data/api';

function App() {
  const [terms, setTerms] = useState([]);

  useEffect(() => {
    getTerms()
      .then(data => {
        setTerms(data.data.map((i: string) => ({value: i, text: i})));
      })
  }, []);

  return (
    <div className="App">
      <Select options={terms} onChange={console.log} />
    </div>
  );
}

export default App;
