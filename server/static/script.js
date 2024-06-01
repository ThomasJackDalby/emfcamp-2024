function sendMessage() {

    let name = document.getElementById("name").innerText;
    let message = document.getElementById("message").innerText;

    let data = {
        styles: [
            {
                "double_height": false,
                "double_width": false,
                "bold": false,
                "align": "left",
                "underline": false
            }
        ],
        commands: [
            { type: "text", content: "Name: "+name, style: 0 },
            { type: "text", content: "Message: "+message, style: 0 },
            { type: "cut" },
        ]
    };

    fetch("http://151.216.211.144:8000/api/print", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        console.log("Request complete! response:", res);
    });
}