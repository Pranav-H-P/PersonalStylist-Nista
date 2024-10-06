const textBox = document.getElementById("textInput");
const sendButton = document.getElementById("sendButton");

const logoText = document.getElementById('logoText');
const content = document.getElementById("mainContent");

const chatBox = document.getElementById("chatContainer");







/*
llmMemory acts as the memory of the llm
It basically does all the recent chat management and localstorage saving stuff

it consists of 2 arrays and 1 string

for bucket 1 and 2 elements are arrays of size 2 holding humanMsg and AIMsg

bucket 1  (supposed to be a queue, but js doesnt have queues??!?!)
latest messages gets added here. Once size reaches qLen, oldest message is popped into bucket 2

bucket 2 - array
messages get added up until it is full. Once it is full it gets summarized and put into the string

string 
holds the summary of the conversation
*/

class llmMemory {

    constructor(qLen, aLen){ // constructor, sets size of buckets and initializes objects with localdata

        const userData = JSON.parse(localStorage.getItem("user"));
    
        this.qLen = qLen;
        this.aLen = aLen;

        this.freshQueue = userData['freshChats'];
        this.summArr = userData['toSummarize'];
        this.summary = userData['summaryText'];

    }

    async addMemory(humanMsg, AIMsg){ // adds a pair of messages to memory
        
        this.freshQueue.push([humanMsg, AIMsg])

        while (this.freshQueue.length > this.qLen){ // freshQueue has exceeded capacity

            let popped = this.freshQueue.shift();
            this.summArr.push(popped);
        }

        if (this.summArr.length > this.aLen){

            try {

                const dataToSummarize = {
                    'toSummarize': this.summArr,
                    'currentSummary': this.summary
                }

                const response = await fetch('/api/getSummary',{ // api to summarize text
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dataToSummarize)
                });
                
                
                if (response.ok){
                    const result = await response.json();
                    this.summary = result['summary'];
                    this.summArr = [] // data has been transfered to summary, so clear it
        
                }else{
                    const result = await response.json();
                    console.log(result.error) // do nothing, wait for the next round to summarize
        
                }
        
            } catch (error) {
                console.log(error) // do nothing, wait for the next round
            }
        
        

        }

        
        console.log(this.freshQueue);
        console.log(this.summArr);
        console.log(this.summary);

        this.saveToDisk() // automatically save data to localStorage so that sending the data is gonna be zero extra steps
    }

    saveToDisk(){ // save data to localStorage
        
        let userData = JSON.parse(localStorage.getItem("user"));
        userData['freshChats'] = this.freshQueue;
        userData['toSummarize'] = this.summArr;
        userData['summaryText'] = this.summary;
        localStorage.setItem("user",JSON.stringify(userData))

    }

    getSummary(){
        return this.summary;
    }
    getFreshChats(){
        return this.freshQueue;
    }
    getToSummarize(){
        return this.freshQueue;
    }
};

let nistaMemory = new llmMemory(5, 5);

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

    let userData = JSON.parse(localStorage.getItem("user"));
    userData['text'] = userInput;


    const userMessage = document.createElement('p'); // create new message
    const nistaMessage = document.createElement('p');

    userMessage.classList.add("message", "human", "comeFromTop");
    nistaMessage.classList.add("message", "ai", "comeFromTop");

    userMessage.innerText = userInput;

    chatBox.append(userMessage);
    

    setTimeout( () => { // wait for a bit for it to load
        userMessage.classList.remove('comeFromTop'); // trigger css transition effect
        chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' }); // scroll to the bottom of the chat box
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

            nistaMessage.innerHTML = result['reply']; // html marked up response
            // original llm generated markdown text is saved in memory
            nistaMemory.addMemory(userInput, result['rawReply']); // add messages to memory

            
        }else{
            const result = await response.json();
            nistaMessage.innerText = result['error'];
            
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
