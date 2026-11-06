// Root React component that will organize the LiveMath interface.
import React from 'react';
import { BrowserRouter, Routes, Route, Link, HashRouter} from 'react-router-dom';
import HomePage from './pages/HomePage.jsx';
import WorkspacePage from './pages/WorkspacePage.jsx';
import { ChatHistManager } from './ChatHistoryManager.jsx';

export default function App() {
    console.log("App component rendered");
    
    return (
        
            <HashRouter>
                <Routes>
                    <Route path="/page" element={<HomePage/>}/>
                    <Route path="/" element={<WorkspacePage/>}/>
                </Routes>
            </HashRouter>
        
    );
    
}

