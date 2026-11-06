export default function ProblemInputForm() {
    console.log("ProblemSetup component rendered");
    const [message, setMessage] = useState("");

    function StartSolvingProcess(e) {
        async (e)=>{
            // Prevent the browser from reloading the page during form submission.
            e.preventDefault();
        
        // Ignore empty or whitespace-only submissions.
            if (message && message.trim().length > 0) {
                // Stop duplicate requests while the current request is still pending.
                if (loading) return; 

                // Set the loading state so the UI knows a request is in progress.
                setLoading(true); 
                write2History(message)
                const userMessage = message;
                setMessage("");

                try{ 
                    // Ask the backend tutor for a reply.
                    const response = await AskTutor(userMessage);
                    write2History(response)
                    console.log(response);

                    
                } catch{
                    write2History("failed to get response")
                }finally{
                    // Always reset the loading flag so the user can send another message.
                    setLoading(false);
                }
                
            }
        };
    }
    
    return(<div id="StartProblemTextDiv">
        <h2>Welcome to LiveMath</h2>
        <form id="StartProblemTextForm">
            <input type="text" id="StartProblemTextInput" name="text"  placeholder="Please enter math problem..."/><br></br>
            <input type="submit" id="StartProblemTextButton" name="Start Solving"/>

        </form>

    </div>)

}