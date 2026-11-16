import { useNavigate } from 'react-router-dom';
import { useState, useContext } from 'react';
import { TextField, Button } from '@mui/material';
import { chatProvider } from '../ChatHistoryManager.jsx';
import { OpeningQuestion } from '../api';

export default function ProblemInputForm() {
    const userRole = "user";
    const aiRole = "ai";
    const navigate = useNavigate();
    const [message, setMessage] = useState("");
    const { history, write2History } = useContext(chatProvider);
    const [loading, setLoading] = useState(false);

    const StartSolvingProcess = async (e)=>{
            // Prevent the browser from reloading the page during form submission.
            
            e.preventDefault();
        
            // Ignore empty or whitespace-only submissions.
            if (message && message.trim().length > 0) {
                if (loading) return;
                setLoading(true); 

                write2History({ role: userRole, content: message });
                const userMessage = message;
                
                setMessage("");
                

                try{ 
                    // Ask the backend tutor for a reply.
                    
                    const response = await OpeningQuestion(userMessage);
                    write2History({ role: aiRole, content: response });
                    navigate('/workit');
                    
                } catch{
                    write2History({ role: aiRole, content: "Failed to get a response." });
                }finally{
                // Always reset the loading flag so the user can send another message.
                setLoading(false);
                }
                
            }
        };

        
    return(
    <div id="StartProblemTextDiv">
        <h2>Welcome to LiveMath</h2>

        <form id="StartProblemTextForm" onSubmit={StartSolvingProcess} >
            {/* Text field where the user types their math question. */}
            <TextField id="StartProblemTextInput" multiline minRows={1} maxRows={4} placeholder="Please enter math problem..."  value={message} onChange={(e) => {
                setMessage(e.target.value);
            }}/>
                            
            <Button id="StartProblemTextButton" type='submit' >
                <p>Start Solving</p>
            </Button>
        </form>
    </div>)

}