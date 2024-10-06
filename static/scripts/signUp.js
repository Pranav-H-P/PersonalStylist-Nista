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
const deleteProfile = document.getElementById("deleteProfile");

const logoText = document.getElementById('logoText');

const submitButton = document.getElementById("submitButton");


if (heading.innerText==="Profile Updation"){ // pre-fill text boxes with old data
    
    deleteProfile.classList.remove('hide');
    let userObj = JSON.parse(localStorage.getItem("user"));

    nameBox.value = userObj['name'];
    ageBox.value = userObj['age'];
    genderBox.value = userObj['gender'];
    ethnicityBox.value = userObj['ethnicity'];
    skinToneBox.value = userObj['skinTone'];
    heightBox.value = userObj['height'];
    sHRIBox.value = userObj['sHR'];
    hHRIBox.value = userObj['hHR'];
    prefBox.value = userObj['prefs'];

}

setTimeout( () => { // wait for a bit for it to load
    content.classList.remove('comeFromLeft'); // trigger css transition effect
    
    deleteProfile.classList.remove('appear');
}, 250);

textForm.addEventListener('submit', async e => { // to get submitted form data

    
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
    
    userObj = {
        'name': userName,
        'age': userAge,
        'gender': userGender,
        'ethnicity': userEthnicity,
        'skinTone': userSkinTone,
        'height': userHeight,
        'sHR': userSHRI,
        'hHR': userhHRI,
        "bodyType": "",
        'prefs': userPrefs,
        'freshChats': [],
        'toSummarize': [],
        'summaryText': ""
    }

    if (heading.innerText==="Profile Updation"){ // if it's updation, dont delete old chat data
        
        let oldObj = JSON.parse(localStorage.getItem("user"));

        userObj['freshChats'] = oldObj['freshChats'];
        userObj['toSummarize'] = oldObj['toSummarize'];
        userObj['summaryText'] = oldObj['summaryText'];

    }
    

    const classificationData = { // data needed for body type classification
        'sHR': userSHRI,
        'hHR': userhHRI,
        'gender': userGender
    };

    submitButton.value = "Saving...";
    try {
        const response = await fetch('/api/getBodyType',{ // api to classify body type
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(classificationData)
        });
        
        
        if (response.ok){
            const result = await response.json();

            submitButton.value = "Saving Sucessful!";

            userObj['bodyType'] = result['bodyType'];

            localStorage.setItem("user",JSON.stringify(userObj)) // save data to localStorage
                                                        // no data is permanently stored in backend
                                                        // its all stored in localStorage
    
            window.location.href = '/chat';


        }else{
            const result = await response.json();
            submitButton.value = result.error;

        }

    } catch (error) {
        submitButton.value = "Something went wrong";
    }


});

imgInput.addEventListener('change', async () => { // uploading image to server
                                                  // will auto fill some fields based on response
    
    imgProcMsg.innerHTML = "Processing image...\nFeel free to fill up your name,\nheight and clothing preferences"

    const img=imgInput.files[0];

    if (!img){
        imgProcMsg.innerText = "Please select an image!";
        return;
    }

    const imgForm = new FormData();
    imgForm.append('image',img);

    try {
        const response = await fetch('/api/processImg',{
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
            sHRIBox.value = result['sHR'];
            hHRIBox.value = result['hHR'];

        }else{
            const result = await response.json();
            imgProcMsg.innerHTML = "Oops, "+ result.error;

        }

    } catch (error) {
        imgProcMsg.innerHTML = "Oops, something went wrong.\nTry again!"
    }



});

deleteProfile.addEventListener('click', () => {

    localStorage.removeItem('user');
    window.location.href = "/";

});

logoText.addEventListener('click', () => {
    window.location.href = "/";
});