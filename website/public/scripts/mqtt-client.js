const hostName = "test.mosquitto.org"
const port = 8080; // MQTT over WebSockets, unencrypted, unauthenticated
const clientID = "12345";
const topic = `Stepper Songs/client${clientID}`;

// create a client instance
const client = new Paho.MQTT.Client(hostName, port, "", clientID);

// called when the client connects
const onConnect = () => {
  // subscript to the stepper songs topic
  client.subscribe(topic);
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

// setup callback for the button
document.getElementById('sendButton').onclick = () => {
  // make message from input field's value
  const messageInput = document.getElementById('messageInput');
  message = new Paho.MQTT.Message(messageInput.value);
  message.destinationName = topic;
  client.publish(message);
  messageInput.value = ''; // clear value at end
};