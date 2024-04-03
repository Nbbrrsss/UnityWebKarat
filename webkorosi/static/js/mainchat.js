// Perbaikan pada file JavaScript
const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#chat-submit"); // Perubahan tombol kirim
const chatLogs = document.querySelector(".chat-logs"); // Tambahan untuk elemen chat logs

sendButton.addEventListener("click", function(event) {
    event.preventDefault(); // Mencegah form untuk submit

    // Mendapatkan teks dari input
    const userText = chatInput.value.trim();
    if (!userText) return; // Menghentikan fungsi jika input kosong

    // Menambahkan pesan dari pengguna ke chat logs
    appendUserMessage(userText);

    // Mengirim permintaan ke views.py untuk mendapatkan respons dari chatbot
    fetch("/inputan_user/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_input: userText })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.bot_response;
        // Menambahkan respons dari chatbot ke chat logs
        appendBotMessage(botResponse);
    })
    .catch(error => console.error("Error:", error));

    // Mengosongkan input setelah pesan dikirim
    chatInput.value = "";
});

function appendUserMessage(message) {
    const userChat = `<div class="chat out">${message}</div>`;
    chatLogs.innerHTML += userChat;
    chatLogs.scrollTop = chatLogs.scrollHeight; // Agar scroll selalu ke bawah
}

function appendBotMessage(message) {
    const botChat = `<div class="chat in">${message}</div>`;
    chatLogs.innerHTML += botChat;
    chatLogs.scrollTop = chatLogs.scrollHeight; // Agar scroll selalu ke bawah
}