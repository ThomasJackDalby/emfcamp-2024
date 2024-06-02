function sendMessage() {

    let name = document.getElementById("name").value;
    let message = document.getElementById("message").value;
    let p = Printer()

    p.style(
        double_height=false,
        double_width=false,
        bold=false,
        align="left",
        underline=false
    );
    p.style(
        double_height=true,
        double_width=true,
        bold=true,
        align="center",
        underline=true
    );
    p.style(
        double_height=false,
        double_width=false,
        bold=false,
        align="center",
        underline=false
    );

    p.text("!! MESSAGE !!", 1)
    p.text("-------------", 2);
    p.text(message);
    p.text("From "+name);
    p.text("-------------", 2);
}

class Printer
{
    constructor() {
        this.commands = [];
        this.styles = [];
    }

    text(text, style=0) {
        this.commands.push({ type: "text", content: text, style: style });
    }

    flush() {
        let request = {
            "styles" : this.commands,
            "commands" : this.styles,
        }
        fetch("http://151.216.211.144:8000/api/print", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(request)
    }).then(res => {
        console.log("Request complete! response:", res);
    });
    }
}

function getAles() {


}