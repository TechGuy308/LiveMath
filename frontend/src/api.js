// Shared functions for communication between the React frontend and Python backend.
import { useEffect, useState } from 'react';

const url = "http://localhost:8000";

// API functions for communicating with the Python backend
async function AskTutor(userMessage){
    console.log(userMessage);
    const response = await fetch(`${url}/ask`, {
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userMessage),
        method: "POST",
    });

    const data = await response.json();
    return data.reply
}

async function OpeningQuestion(userMessage){
    const response = await fetch(`${url}/opener`, {
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userMessage),
        method: "POST",
    });
    
    const data = await response.json();
    return data.reply
}

async function Vision(imageBlob) {
    const formData = new FormData();
    formData.append('image', imageBlob);
    

    const response = await fetch(`${url}/vision`, {
        method: "POST",
        body: formData,
    });

    const data = await response.json();
    return data.reply
}

export {AskTutor, OpeningQuestion, Vision};
