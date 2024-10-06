const textBox = document.getElementById("textInput");
const sendButton = document.getElementById("sendButton");

const logoText = document.getElementById('logoText');
const content = document.getElementById("mainContent");


setTimeout( () => { // wait for a bit for it to load
    content.classList.remove('comeFromBottom'); // trigger css transition effect
    
}, 250);


logoText.addEventListener('click', () => {
    window.location.href = "/";
});

textBox.addEventListener('keydown', e => {
    
    if (e.key === 'Enter') {
      
      e.preventDefault(); // Prevent the default behavior of the Enter key (next line)
      
      sendButton.click();
    }
});
  
sendButton.addEventListener('click', () => {

    console.log("sending to server");

});
