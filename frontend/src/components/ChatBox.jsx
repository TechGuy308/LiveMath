// React component for the math tutor conversation interface.
// This panel handles the user chat experience, message submission, and the live conversati
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import { TextField, Button } from '@mui/material';
import TelegramIcon from '@mui/icons-material/Telegram';
import { AskTutor } from '../api';
import Draggable from 'react-draggable';
import { useState, useRef, useContext } from "react";
import { chatProvider } from '../ChatHistoryManager.jsx';

// Main chat component that renders the draggable tutor window.
export default function Chat(){
    // Tracks the current text value in the input field before submission.
    const [message, setMessage] = useState("");
    const { history, write2History } = useContext(chatProvider);
    
    

    // Prevents duplicate sends while the app is waiting on a tutor response.
    const [loading, setLoading] = useState(false);
    
    // Holds the DOM reference for the draggable chat container.
    const nodeRef = useRef(null);

    // Sends the user's typed question to the backend tutor and appends the response to chat history.
    const SendMessage = async (e)=>{
        // Prevent the browser from reloading the page during form submission.
        e.preventDefault();
        
        // Ignore empty or whitespace-only submissions.
        if (message && message.trim().length > 0) {
            // Stop duplicate requests while the current request is still pending.
            if (loading) return; 
            setLoading(true); 

            write2History(message)
            const userMessage = message;
            setMessage("");

            try{ 
                // Ask the backend tutor for a reply.
                const response = await AskTutor(userMessage);
                write2History(response)  
            } catch{
                write2History("failed to get response")
            }finally{
                // Always reset the loading flag so the user can send another message.
                setLoading(false);
            }
            
        }
    };
    
    // Renders the chat window, transcript, and input form.
    return (<Draggable nodeRef={nodeRef}>
            {/* Outer draggable container for the floating chat panel. */}
            <div id='ChatDiv' ref={nodeRef}>
                {/* Main conversation area where each message is displayed. */}
                <div id="ChatArea">
                    
                    {history.length > 0 ? (
                        // Render the full chat transcript when messages exist.
                        <section className="chatHistorySection">
                        {history.map((message, index) => (
                            // Alternate styling between user messages and tutor responses.
                            <p key={index} className={(index+1) % 2 == 0 ? "response" : "query"}>{message}</p>
                        ))}
                        </section>
                    ) : (
                        // Empty-state layout before the first message is sent.
                        <section className="my-10 main">
                        <AutoAwesomeIcon fontSize="large" color="warning"></AutoAwesomeIcon>
                        <h1 className="mb-10">Ask me anything</h1>
                        </section>
                    )}
                </div>
                
                {/* Input form for the user's next message to the tutor. */}
                <form id='ChatForm' onSubmit={SendMessage} >
                    {/* Text field where the user types their math question. */}
                    <TextField id="outlined-basic" variant="outlined" multiline minRows={1} maxRows={4} placeholder='Ask the Tutor a Question...' value={message} onChange={(e) => {
                            setMessage(e.target.value);
                    }}/>
                    
                    {/* Submit button that sends the user's message to the backend. */}
                    <Button id='ChatSubmit' type='submit' endIcon={<TelegramIcon/>}/>
                </form>
            
        </div>
    </Draggable>)
}