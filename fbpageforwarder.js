const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

// Telegram Bot Token
const TELEGRAM_BOT_TOKEN = "<telegrambot token>";

// Facebook Page Access Token and Page ID
const FACEBOOK_PAGE_ACCESS_TOKEN = "<FB access token>";

const FACEBOOK_PAGE_ID = "520852677783384";
//const FACEBOOK_PAGE_ID = "61570407073446";
// Webhook URL for Telegram
const WEBHOOK_URL = "https://telegrambot-fbpageforwarder.glitch.me/webhook";

// Set Telegram Webhook
async function setWebhook() {
    try {
        const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook`;
        const response = await axios.post(url, { url: WEBHOOK_URL });
        if (response.data.ok) {
            console.log("Telegram webhook set successfully!");
        } else {
            console.error("Failed to set Telegram webhook:", response.data);
        }
    } catch (error) {
        console.error("Error setting Telegram webhook:", error.message);
    }
}

// Post message to Facebook
async function postToFacebook(message) {
    try {
        const url = `https://graph.facebook.com/v21.0/${FACEBOOK_PAGE_ID}/feed`;
        const response = await axios.post(url, {
            message: message,
            access_token: FACEBOOK_PAGE_ACCESS_TOKEN,
        });
        if (response.status === 200) {
            console.log("Message posted to Facebook successfully!");
        } else {
            console.error("Failed to post to Facebook:", response.data);
        }
    } catch (error) {
        console.error("Error posting to Facebook:", error.message);
    }
}

// Handle Telegram Webhook
app.post('/webhook', async (req, res) => {
    try {
        const update = req.body;

        // Check if the update is a channel post
        if (update.channel_post && update.channel_post.text) {
            const text = update.channel_post.text;
            console.log("New message from Telegram channel:", text);

            // Post the message to Facebook
            await postToFacebook(text);
        }

        res.sendStatus(200); // Respond with 200 OK
    } catch (error) {
        console.error("Error processing webhook:", error.message);
        res.sendStatus(500); // Respond with 500 Internal Server Error
    }
});

// Start the Express server
const PORT = 3000;
app.listen(PORT, async () => {
    console.log(`Server running on port ${PORT}`);

    // Set the Telegram webhook when the server starts
    await setWebhook();
});
