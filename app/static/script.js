// Copy code
const btn = document.getElementById("copyBtn")

if(btn){
    btn.onclick = () => {
        const text = document.querySelector("pre").innerText

        navigator.clipboard.writeText(text)

        btn.innerText = "Copied!"
    }

}

// Theme toggle
const toggle = document.getElementById("themeToggle")

if(toggle){
    toggle.onclick = () => {
        document.body.classList.toggle("light")

        localStorage.setItem(
            "theme",
            document.body.classList.contains("light") ? "light":"dark"
        )

    }

    if(localStorage.getItem("theme")==="light"){
        document.body.classList.add("light")
    }
}