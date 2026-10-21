// Root React component that will organize the LiveMath interface.
import React from 'react';
import { BrowserRouter, Routes, Route, Link, HashRouter} from 'react-router-dom';
import ProblemSetup from './pages/StartPage';
import Workbench from './pages/WorkStation';


export default function App() {
    console.log("App component rendered");
    return (
        <HashRouter>
            <Routes>
                <Route path="/page" element={<ProblemSetup/>}/>
                <Route path="/" element={<Workbench/>}/>
            </Routes>
        </HashRouter>
    );
    
}



