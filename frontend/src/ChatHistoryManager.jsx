import { useState, createContext } from "react";
export const chatProvider = createContext();


export default function ChatHistManager({children}){
    const [history, setHistory] = useState([]);
    function write2History(message){
        setHistory((prev)=> [...prev, message]);
    }
    return <div>
        <chatProvider.Provider value={{history, write2History}}>
            {children}
        </chatProvider.Provider>
    </div>

}