// Root React component that will organize the LiveMath interface.
import React from 'react';
import {Routes, Route, HashRouter} from 'react-router-dom';
import HomePage from './pages/HomePage.jsx';
import WorkspacePage from './pages/WorkspacePage.jsx';
import ChatHistManager from './ChatHistoryManager.jsx';

export default function App() {
    
    
    return (
        <ChatHistManager>
            <HashRouter>
                <Routes>                   
                    <Route path="/" element={<HomePage/>}/>
                    <Route path="/workit" element={<WorkspacePage/>}/>
                </Routes>
            </HashRouter>
        </ChatHistManager>
    );
    
}

