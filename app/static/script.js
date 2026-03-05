// Copy code
const btn = document.getElementById("copyBtn")

if (btn) {
    btn.onclick = () => {
        let text = ""

        const codeLines = document.querySelectorAll(".code-pre .line .code")
        if (codeLines.length > 0) {
            text = Array.from(codeLines, (line) => line.textContent).join("\n")
        } else {
            const pre = document.querySelector("pre")
            text = pre ? pre.innerText : ""
        }

        navigator.clipboard.writeText(text)
        btn.innerText = "Copied!"
    }
}

// Theme toggle
const toggle = document.getElementById("themeToggle")

if (toggle) {
    toggle.onclick = () => {
        document.body.classList.toggle("light")

        localStorage.setItem(
            "theme",
            document.body.classList.contains("light") ? "light" : "dark"
        )
    }

    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light")
    }
}
