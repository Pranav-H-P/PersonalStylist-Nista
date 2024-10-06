const textBox = document.getElementById("textInput");
const sendButton = document.getElementById("sendButton");

const logoText = document.getElementById('logoText');
const content = document.getElementById("mainContent");

const chatBox = document.getElementById("chatContainer");

setTimeout( () => { // wait for a bit for it to load
    content.classList.remove('comeFromBottom'); // trigger css transition effect
    
}, 250);


logoText.addEventListener('click', () => {
    window.location.href = "/";
});

textBox.addEventListener('keydown', e => {
    
    const userAgent = navigator.userAgent;
    if (!userAgent.match(/Mobile|Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i)){ // exclude mobile users from this

        if (e.key === 'Enter' && !e.shiftKey ) { // Enter key sends message on PC, shift+enter creates new line
        
        e.preventDefault(); // Prevent the default behavior of the Enter key (new line)
        
        sendButton.click();
        }
    }
});
  
sendButton.addEventListener('click', async () => {

    const userInput = textBox.value.trim();

    if (userInput === ""){
        return;
    }

    textBox.value = "";
    textBox.disabled = true;
    sendButton.disabled = true;

    let userData = {};
    userData['text'] = userInput


    const userMessage = document.createElement('p'); // create new message
    const nistaMessage = document.createElement('p');

    userMessage.classList.add("message", "human", "comeFromTop");
    nistaMessage.classList.add("message", "ai", "comeFromTop");

    userMessage.innerText = userInput;

    chatBox.append(userMessage);

    setTimeout( () => { // wait for a bit for it to load
        userMessage.classList.remove('comeFromTop'); // trigger css transition effect
    }, 200);
    
    

    try { // get llm response
        const response = await fetch("/api/getNistaResponse",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        
        if (response.ok){
            const result = await response.json(); // returns html tags which were made from markdown

            nistaMessage.innerHTML = result['reply']; 
            
        }else{
            const result = await response.json();
            nistaMessage.innerText = result['reply'];
            
        }

    } catch (error) {
        nistaMessage.innerText = "Something went wrong, the server couldn't be accessed!";
        console.log("error");
    }

    chatBox.append(nistaMessage);

    
    setTimeout( () => { // wait for a bit for it to load
        nistaMessage.classList.remove('comeFromTop'); // trigger css transition effect
    }, 250);
    
    
    textBox.disabled = false;
    sendButton.disabled = false;
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' }); // scroll to bottom of the chatbox
});
