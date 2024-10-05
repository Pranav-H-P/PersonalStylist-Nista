const imageForm = document.getElementById('imgForm');
const textForm = document.getElementById('textForm');

const content = document.getElementById('mainContent');
const heading = document.getElementById("formHeading");

const nameBox = document.getElementById("nameInput");
const ageBox = document.getElementById("ageInput");
const genderBox = document.getElementById("genderInput");
const ethnicityBox = document.getElementById("ethnicityInput");
const skinToneBox = document.getElementById("skinInput");
const heightBox = document.getElementById("heightInput");
const sHRIBox = document.getElementById("sHRIInput");
const wHRIBox = document.getElementById("wHRIInput");
const prefBox = document.getElementById("preferenceInput");



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
    wHRIBox.value = userObj['wHRI'];
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
    const userSHRI = data.get('sHRIInput'); // shoulder to height ratio
    const userWHRI = data.get('wHRIInput'); // waist to height ratio
    const userPrefs = data.get('preferenceInput');

    let userObj = {};

    userObj['user'] = {
        'name': userName,
        'age': userAge,
        'gender': userGender,
        'ethnicity': userEthnicity,
        'skinTone': userSkinTone,
        'height': userHeight,
        'sHRI': userSHRI,
        'wHRI': userWHRI,
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

