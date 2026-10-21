//This page will render Canvas and Chatbox
import WhiteBoard from '../components/MathCanvas.jsx';
import Chat from '../components/ChatPanel.jsx';
import useState from 'react';

export default function Workbench(){
    const [parentChatHistory, addParentChatHistory] = useState("");
    
    return(<div>
        {/* Whiteboard for mathematical computations and visualizations */}
        <WhiteBoard/>
        
        {/* Chat panel for interacting with the tutor */}
        <Chat/>
    </div>
    );
}