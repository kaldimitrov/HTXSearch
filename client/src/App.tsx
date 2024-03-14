import React from 'react';
import SearchBar from './components/SearchBar';
import './App.css';

function App() {
  return (
    <div className="body">
      <div className="text">
        <p>
          HTXSearch
        </p>
      </div>
      <div className="search-bar">
        <SearchBar />
      </div>
    </div>
  );
}

export default App;
