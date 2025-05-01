/*
MQTT Client Script
-------------------
This script handles the MQTT client connection for the web application.
It allows users to send musical notes to the MQTT broker and interact with the virtual piano.

Kenny Howes - kenneth.howes53@gmail.com
Omar Valdez - ov25@calvin.edu
*/

const hostName = "iot.cs.calvin.edu"
const port = 8080;
let topic = `Stepper Songs/null`;

const updateTopic = () => {
  const clientID = document.getElementById("clientIDInput").value;
  if (clientID === "")
    throw "ClientID is empty";

  topic = `Stepper Songs/client${clientID}`;
  console.log(`Changed topic to: ${topic}`);
}

const disableKeys = () => {
  document.querySelectorAll('.key').forEach(key => {
    key.classList.add('is-disabled');
    key.disabled = true;
  });
}

const enableKeys = () => {
  document.querySelectorAll('.key').forEach(key => {
    key.classList.remove('is-disabled');
    key.disabled = false;
  });
}

/* procedural code to be run at startup */
disableKeys();

// create a client instance
const client = new Paho.MQTT.Client(hostName, port, "", "");

// called when the client connects
const onConnect = () => {
  console.log("MQTT connected");
}

// called when the client loses its connection
const onConnectionLost = (responseObject) => {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
const onMessageArrived = (message) => {
  const messagesList = document.getElementById('messagesList');
  const messageItem = document.createElement('div');
  messageItem.textContent = message.payloadString;
  messagesList.appendChild(messageItem);
}

// set cb's
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client


// Add event listeners to piano keys to play them
const defaultNoteDuration = 100; // milliseconds
document.querySelectorAll('.key').forEach(key => {
    let intervalHandle;

    // have the button continuously publish the note when pressed
    // and stop when released
    key.addEventListener('mousedown', () => {
      if (!client.isConnected()) {
        console.error("MQTT not connected");
        return;
      }
      if (topic === `Stepper Songs/null`) {
        console.error("No clientID set");
        return;
      }

      const note = key.dataset.note + "--" + String(defaultNoteDuration);
      intervalHandle = setInterval(() => {
        const message = new Paho.MQTT.Message(note);
        message.destinationName = topic;
        client.publish(message);
        console.log(`Published note: ${note}`);
      }, defaultNoteDuration);
    });

    key.addEventListener('mouseup', () => {
      clearInterval(intervalHandle);
    });

    key.addEventListener('mouseleave', () => {
      clearInterval(intervalHandle);
    });
});

// setup connect and disconnect buttons
document.getElementById("connectButton").addEventListener("click", () => {
  updateTopic();

  const username = document.getElementById("usernameInput").value;
  const password = document.getElementById("passwordInput").value;
  client.connect({
    userName: username,
    password: password,
    onSuccess: onConnect
  });

  enableKeys();
});

document.getElementById("disconnectButton").addEventListener("click", () => {
  disableKeys();
  topic = `Stepper Songs/null`;
  document.getElementById("clientIDInput").value = "";
  client.disconnect();
  console.log("MQTT disconnected");
});
