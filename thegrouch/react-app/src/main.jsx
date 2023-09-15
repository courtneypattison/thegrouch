import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import Categories from "./categories";


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <div className="bg-gray-100">
    <Categories />
    </div>
  </React.StrictMode>,
)
