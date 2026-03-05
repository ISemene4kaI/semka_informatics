const THEME_KEY = "theme"
const toggle = document.getElementById("themeToggle")
const copyBtn = document.getElementById("copyBtn")
const hljsTheme = document.getElementById("hljsTheme")

function applyTheme(theme) {
    document.body.classList.toggle("light", theme === "light")

    if (toggle) {
        toggle.textContent = theme === "light" ? "☀️" : "🌙"
    }

    if (hljsTheme) {
        hljsTheme.href = theme === "light"
            ? "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css"
            : "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css"
    }
}

const savedTheme = localStorage.getItem(THEME_KEY)
const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches
const initialTheme = savedTheme || (prefersLight ? "light" : "dark")
applyTheme(initialTheme)

if (toggle) {
    toggle.onclick = () => {
        const nextTheme = document.body.classList.contains("light") ? "dark" : "light"
        applyTheme(nextTheme)
        localStorage.setItem(THEME_KEY, nextTheme)
    }
}

// Copy code
if (copyBtn) {
    copyBtn.onclick = () => {
        let text = ""

        const codeLines = document.querySelectorAll(".code-pre .line .code")
        if (codeLines.length > 0) {
            text = Array.from(codeLines, (line) => line.textContent).join("\n")
        } else {
            const pre = document.querySelector("pre")
            text = pre ? pre.innerText : ""
        }

        navigator.clipboard.writeText(text)
        copyBtn.textContent = "Copied!"
    }
}
