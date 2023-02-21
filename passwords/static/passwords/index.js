const copyContent = async (value) => {
    try {
        let text = document.getElementsByClassName("myText")[value-1].innerText;
        await navigator.clipboard.writeText(text);
        document.getElementsByClassName("copyButton")[value-1].innerText = "copied";
    } catch (err) {
      alert("Failed to copy. Check your browser's settings");
    }
}

