const imageForm = document.getElementById('imgForm');
const textForm = document.getElementById('textForm');
const content = document.getElementById('mainContent');


textForm.addEventListener('submit', e => {

    console.log("captured text form lol")
    e.preventDefault(); 

})

content.classList.remove('comeFromLeft');