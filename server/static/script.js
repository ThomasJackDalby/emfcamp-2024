function sendMessage() {

    let name = document.getElementById("name").value;
    let message = document.getElementById("message").value;

    let data = {
        styles: [
            {
                "double_height": false,
                "double_width": false,
                "bold": false,
                "align": "left",
                "underline": false
            },
            {
                "double_height": true,
                "double_width": true,
                "bold": true,
                "align": "center",
                "underline": true
            },
            {
                "double_height": false,
                "double_width": false,
                "bold": false,
                "align": "center",
                "underline": false
            }
        ],
        commands: [
            { type: "text", content: "!! MESSAGE !!", style: 1 },
            { type: "text", content: "-------------", style: 2 },
            { type: "text", content: message, style: 0 },
            { type: "text", content: "From "+name, style: 0 },
            { type: "text", content: "-------------", style: 2 },
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