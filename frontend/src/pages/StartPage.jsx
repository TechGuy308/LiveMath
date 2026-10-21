// React component for entering and starting a math problem.

import useState from "react"
let Question

function StartSolvingProcess(e) {
    setMytxt(e.target.value);
}

export default function ProblemSetup() {
    console.log("ProblemSetup component rendered");
    const [mytxt, setMytxt] = useState("");
    
    return(<div id="StartProblemTextDiv">
        <h2>Welcome to LiveMath</h2>
        <form id="StartProblemTextForm">
            <input type="text" id="StartProblemTextInput" name="text"  placeholder="Please enter math problem..."/><br></br>
            <input type="submit" id="StartProblemTextButton" name="Start Solving"/>

        </form>

    </div>)

}