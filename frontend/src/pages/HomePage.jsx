// React component for entering and starting a math problem.
import ProblemInputForm from '../components/ProblemInputForm.jsx';
import { ChatHistManager } from '../ChatHistoryManager.jsx';

export default function HomePage(){
    return(<div>
        <ChatHistManager>
            <ProblemInputForm/>
        </ChatHistManager>
        
    </div>
    );
}

