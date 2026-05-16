const express = require("express");
const cors = require("cors");
const fs = require("fs");
const { v4: uuidv4 } = require("uuid");

const app = express();

app.use(cors());
app.use(express.json());


// SIGNUP API
app.post("/signup", (req, res) => {
  const {
    username,
    password,
    nativeLanguage,
    learningLanguage
  } = req.body;

  const users = JSON.parse(
    fs.readFileSync("./data/users.json")
  );

  // check existing user
  const existingUser = users.find(
    (u) => u.username === username
  );

  if (existingUser) {
    return res.status(400).json({
      success: false,
      message: "Username already exists"
    });
  }

  const newUser = {
    id: uuidv4(),
    username,
    password,
    nativeLanguage,
    learningLanguage
  };

  users.push(newUser);

  fs.writeFileSync(
    "./data/users.json",
    JSON.stringify(users, null, 2)
  );

  res.json({
    success: true,
    message: "Signup successful",
    user: newUser
  });
});


// LOGIN API
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  const users = JSON.parse(
    fs.readFileSync("./data/users.json")
  );

  const user = users.find(
    (u) =>
      u.username === username &&
      u.password === password
  );

  if (user) {
    res.json({
      success: true,
      user
    });
  } else {
    res.status(401).json({
      success: false,
      message: "Invalid credentials"
    });
  }
});


// MATCH USERS
app.get("/matches/:id", (req, res) => {
  const users = JSON.parse(
    fs.readFileSync("./data/users.json")
  );

  const currentUser = users.find(
    (u) => u.id == req.params.id
  );

  if (!currentUser) {
    return res.status(404).json({
      message: "User not found"
    });
  }

  const matches = users.filter(
    (u) =>
      u.id !== currentUser.id &&
      u.nativeLanguage ===
        currentUser.learningLanguage &&
      u.learningLanguage ===
        currentUser.nativeLanguage
  );

  res.json(matches);
});


// SEND MESSAGE
app.post("/chat", (req, res) => {
  const { sender, receiver, message } = req.body;

  const chats = JSON.parse(
    fs.readFileSync("./data/chats.json")
  );

  const newMessage = {
    sender,
    receiver,
    message,
    time: new Date()
  };

  chats.push(newMessage);

  fs.writeFileSync(
    "./data/chats.json",
    JSON.stringify(chats, null, 2)
  );

  res.json({
    success: true,
    newMessage
  });
});


// GET CHATS
app.get("/chat", (req, res) => {
  const chats = JSON.parse(
    fs.readFileSync("./data/chats.json")
  );

  res.json(chats);
});


// TEST ROUTE
app.get("/", (req, res) => {
  res.send("Language Exchange Backend Running");
});


const PORT = 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});