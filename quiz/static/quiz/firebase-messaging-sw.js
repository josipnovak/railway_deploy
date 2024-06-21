importScripts('https://www.gstatic.com/firebasejs/8.6.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.6.1/firebase-messaging.js');

firebase.initializeApp({
  apiKey: "AIzaSyBcSUZ0zXsAEOY9t4PL82NqBKdGJFZgsX0",
  authDomain: "zavrsni-proba-1.firebaseapp.com",
  databaseURL: "https://zavrsni-proba-1-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "zavrsni-proba-1",
  storageBucket: "zavrsni-proba-1.appspot.com",
  messagingSenderId: "649829209184",
  appId: "1:649829209184:web:343823581c648622d65f05"
});

const messaging = firebase.messaging();