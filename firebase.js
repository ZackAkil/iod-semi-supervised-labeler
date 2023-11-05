import { initializeApp } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-app.js";
// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);


import { getStorage, ref, uploadString } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-storage.js";


const storage = getStorage(firebaseApp, BUCKET);


export function upload_file(name, dataUrl, bboxes = '') {

    const storageRef = ref(storage, name);

    const metadata = {
        contentType: 'image/png',
        customMetadata: {
            'labels': JSON.stringify(bboxes)
        }
    };

    uploadString(storageRef, dataUrl, 'data_url', metadata).then((snapshot) => {
        console.log('Uploaded a data_url string! ✅ :', name);
    });

}

// const name = 'hi'
// const dataUrl = 'data:text/plain;base64,5b6p5Y+344GX44G+44GX44Gf77yB44GK44KB44Gn44Go44GG77yB'
// const bbox = 'hello'
// upload_file(name, dataUrl, bbox)