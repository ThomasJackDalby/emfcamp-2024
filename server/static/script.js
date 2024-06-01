function sendMessage() {
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
            { type: "text", content: "Browser test message", style: 0 },
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