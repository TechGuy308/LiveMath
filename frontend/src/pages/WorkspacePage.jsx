//This page will render Canvas and Chatbox
import MathWhiteboard from '../components/MathWhiteboard.jsx';
import Chat from '../components/ChatBox.jsx';
import { ChatHistManager } from '../ChatHistoryManager.jsx';

export default function WorkspacePage(){
    return(<div>
        {/* Whiteboard for mathematical computations and visualizations */}
        <ChatHistManager>
            <MathWhiteboard/>
            <Chat/>
        </ChatHistManager>
        
    </div>
    );
}