// Shared functions for communication between the React frontend and Python backend.

const url = "https://livemathbackend.onrender.com";

// API functions for communicating with the Python backend
async function AskTutor(userMessage){
    try{
        const response = await fetch(`${url}/ask`, {
        headers: {"Content-Type": "application/json",},
        body: JSON.stringify(userMessage),
        method: "POST",
        });
        
        if (response.ok){
            const data = await response.json();
            return data.reply
        }else{
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    }catch{
        
    }
    
    
}

async function OpeningQuestion(userMessage){
    const response = await fetch(`${url}/opener`, {
        headers: {"Content-Type": "application/json",},
        body: JSON.stringify(userMessage),
        method: "POST",
    });
    
    if (response.ok){
        const data = await response.json();
        return data.reply
    }else{
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
}

async function Vision(imageBlob) {
    const formData = new FormData();
    formData.append('image', imageBlob);
    

    const response = await fetch(`${url}/vision`, {
        method: "POST",
        body: formData,
    });

    if (response.ok){
        const data = await response.json();
        return data.reply
    }else{
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
}

export {AskTutor, OpeningQuestion, Vision};
