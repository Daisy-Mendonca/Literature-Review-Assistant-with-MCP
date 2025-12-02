async function sendQuery() {
    const q = document.getElementById("query").value;
    const output = document.getElementById("output");
    output.textContent = "Thinking...";

    try {
        const response = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q })
        });

        const result = await response.json();
        document.getElementById("output").textContent = 
        JSON.stringify(result, null, 2);
    }
    catch (error) {
        document.getElementById("output").textContent = 
        "Error: " + error.message;
    }
}