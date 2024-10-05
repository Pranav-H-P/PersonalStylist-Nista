const textForm = document.getElementById('textForm');

const content = document.getElementById('mainContent');
const heading = document.getElementById("formHeading");

const nameBox = document.getElementById("nameInput");
const ageBox = document.getElementById("ageInput");
const genderBox = document.getElementById("genderInput");
const ethnicityBox = document.getElementById("ethnicityInput");
const skinToneBox = document.getElementById("skinInput");
const heightBox = document.getElementById("heightInput");
const sHRIBox = document.getElementById("sHRIInput"); // shoulder to hip ratio
const hHRIBox = document.getElementById("hHRIInput"); // hip to height ratio
const prefBox = document.getElementById("preferenceInput");

const imgInput = document.getElementById("imgInput");
const imgProcMsg = document.getElementById("imgProcessStatus");


setTimeout( () => { // wait for bit for it to load
        content.classList.remove('comeFromLeft'); // trigger css transition effect
}, 250)


if (heading.innerText==="Profile Updation"){ // pre-fill text boxes with old data

    let userObj = JSON.parse(localStorage.getItem("user"))['user'];

    nameBox.value = userObj['name'];
    ageBox.value = userObj['age'];
    genderBox.value = userObj['gender'];
    ethnicityBox.value = userObj['ethnicity'];
    skinToneBox.value = userObj['skinTone'];
    heightBox.value = userObj['height'];
    sHRIBox.value = userObj['sHRI'];
    hHRIBox.value = userObj['hHRI'];
    prefBox.value = userObj['prefs'];

}



textForm.addEventListener('submit', e => { // to get submitted form data

    
    e.preventDefault(); // stop form from refreshing page
                        // and/or making requests by itself

    const data = new FormData(textForm);


    const userName = data.get('nameInput');
    const userAge = data.get('ageInput');
    const userGender = data.get('genderInput');
    const userEthnicity = data.get('ethnicityInput');
    const userSkinTone = data.get('skinInput');
    const userHeight = data.get('heightInput');
    const userSHRI = data.get('sHRIInput'); // shoulder to hip ratio
    const userhHRI = data.get('hHRIInput'); // hip to height ratio
    const userPrefs = data.get('preferenceInput');

    let userObj = {};

    /*
        TODO
    ================
    ADD LLM PROCESSING TO PROPERLY PROCESS AND FORMAT THIS DATA
    SO THAT IT CAN BE FED INTO THE ML ALGORITHM PROPERLY
    */ 

    userObj['user'] = {
        'name': userName,
        'age': userAge,
        'gender': userGender,
        'ethnicity': userEthnicity,
        'skinTone': userSkinTone,
        'height': userHeight,
        'sHRI': userSHRI,
        'hHRI': userhHRI,
        'prefs': userPrefs,
        'chatSummary': "",
        'last10Outfits': [

        ]
    }
    
    localStorage.setItem("user",JSON.stringify(userObj)) // save data to localStorage
                                                        // no data is permanently stored in backend
                                                        // its all stored in localStorage
    
   window.location.href = '/chat';
})

imgInput.addEventListener('change', async () => { // uploading image to server
                                                  // will auto fill some fields based on response
    
    imgProcMsg.innerHTML = "Processing image..."

    const img=imgInput.files[0];

    if (!img){
        imgProcMsg.innerText = "Please select an image!";
        return;
    }

    const imgForm = new FormData();
    imgForm.append('image',img);

    try {
        const response = await fetch('/processImg',{
            method: 'POST',
            body: imgForm
        });
        
        
        if (response.ok){
            const result = await response.json();

            imgProcMsg.innerHTML = "Success! Please verify the data.";

            ageBox.value = result['age'];
            genderBox.value = result['gender'];
            ethnicityBox.value = result['ethnicity'];
            skinToneBox.value = result['skinTone'];
            sHRIBox.value = result['sHRI'];
            hHRIBox.value = result['hHRI'];

        }else{
            const result = await response.json();
            imgProcMsg.innerHTML = "Oops, "+ result.error;

        }

    } catch (error) {
        imgProcMsg.innerHTML = "Oops, something went wrong.\nTry again!"
    }



})