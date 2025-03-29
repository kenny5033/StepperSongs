const hostName = "test.mosquitto.org"
const port = 8080; // MQTT over WebSockets, unencrypted, unauthenticated
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
client.connect({onSuccess:onConnect});

// Add event listeners to piano keys to play them
document.querySelectorAll('.key').forEach(key => {
    key.addEventListener('click', () => {
        if (!client.isConnected()) {
            console.error("MQTT not connected");
            return;
        }
        if (topic === `Stepper Songs/null`) {
            console.error("No clientID set");
            return
        }
        const note = key.dataset.note;
        const message = new Paho.MQTT.Message(note);
        message.destinationName = topic;
        client.publish(message);
        console.log(`Published note: ${note}`);
    });
});

// setup connect and disconnect buttons
document.getElementById("connectButton").addEventListener("click", () => {updateTopic(); enableKeys();});
document.getElementById("disconnectButton").addEventListener("click", () => {
  topic = `Stepper Songs/null`;
  document.getElementById("clientIDInput").value = "";
  disableKeys();
});
