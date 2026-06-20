const THEME_KEY = "theme";
const toggle = document.getElementById("themeToggle");
const copyBtn = document.getElementById("copyBtn");
const hljsTheme = document.getElementById("hljsTheme");

function applyTheme(theme) {
    document.body.classList.toggle("light", theme === "light");

    if (toggle) {
        toggle.textContent = theme === "light" ? "☀️" : "🌙";
    }

    if (hljsTheme) {
        hljsTheme.href = theme === "light"
            ? "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css"
            : "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css";
    }
}

const savedTheme = localStorage.getItem(THEME_KEY);
const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
const initialTheme = savedTheme || (prefersLight ? "light" : "dark");
applyTheme(initialTheme);

if (toggle) {
    toggle.onclick = () => {
        const nextTheme = document.body.classList.contains("light") ? "dark" : "light";
        applyTheme(nextTheme);
        localStorage.setItem(THEME_KEY, nextTheme);
    };
}

if (window.hljs) {
    document.querySelectorAll(".markdown-body pre code").forEach((block) => {
        window.hljs.highlightElement(block);
    });

    document.querySelectorAll(".code-pre .code").forEach((line) => {
        if (line.textContent) {
            window.hljs.highlightElement(line);
        }
    });
}

function showCopyResult(message) {
    copyBtn.textContent = message;
    window.setTimeout(() => {
        copyBtn.textContent = "📋 Копировать";
    }, 1600);
}

if (copyBtn) {
    copyBtn.onclick = async () => {
        let text = "";

        const codeLines = document.querySelectorAll(".code-pre .line .code");
        if (codeLines.length > 0) {
            text = Array.from(codeLines, (line) => line.textContent).join("\n");
        } else {
            const pre = document.querySelector("pre");
            text = pre ? pre.innerText : "";
        }

        try {
            await navigator.clipboard.writeText(text);
            showCopyResult("✓ Скопировано");
        } catch {
            showCopyResult("Не удалось скопировать");
        }
    };
}
