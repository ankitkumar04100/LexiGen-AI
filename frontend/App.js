// frontend/App.js
// Minimal vanilla-React-like single-file demo using no build system (for quick demo).
// If you prefer React+create-react-app, copy the JSX into a proper component.

(function () {
  // Simple DOM UI
  const root = document.getElementById("root");
  root.innerHTML = `
    <div style="font-family: Arial, sans-serif; max-width:760px; margin:40px auto;">
      <h1>LexiGen AI - Demo</h1>
      <p>Upload a text file (.txt) to demo summarization (demo mode).</p>
      <input id="fileInput" type="file" accept=".txt,.pdf,.docx" />
      <button id="uploadBtn">Upload & Summarize</button>
      <div id="result" style="margin-top:20px"></div>
      <hr />
      <h3>Ask a question</h3>
      <input id="docIdInput" placeholder="Enter doc_id from upload" style="width:300px" />
      <input id="queryInput" placeholder="Type question" style="width:300px; margin-left:8px" />
      <button id="askBtn">Ask</button>
      <div id="qaResult" style="margin-top:10px"></div>
    </div>
  `;

  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");
  const resultDiv = document.getElementById("result");
  const askBtn = document.getElementById("askBtn");

  uploadBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) {
      alert("Choose a file (txt for demo).");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    resultDiv.innerHTML = "Uploading...";
    try {
      const res = await fetch("http://localhost:5000/api/v1/upload", {
        method: "POST",
        body: formData
      });
      const j = await res.json();
      if (res.ok) {
        resultDiv.innerHTML = `<b>Uploaded:</b> ${j.filename} <br><b>Doc ID:</b> ${j.doc_id} <br>Fetching summary...`;
        const summ = await fetch(`http://localhost:5000/api/v1/summary/${j.doc_id}`);
        const summJ = await summ.json();
        if (summ.ok) {
          resultDiv.innerHTML += `<pre style="background:#f6f6f6; padding:10px;">${summJ.summary}</pre>`;
        } else {
          resultDiv.innerHTML += `<div>Error getting summary</div>`;
        }
      } else {
        resultDiv.innerHTML = `<div>Error uploading file: ${j.error}</div>`;
      }
    } catch (e) {
      resultDiv.innerHTML = `Error: ${e.message}`;
    }
  });

  askBtn.addEventListener("click", async () => {
    const docId = document.getElementById("docIdInput").value.trim();
    const query = document.getElementById("queryInput").value.trim();
    if (!docId || !query) {
      alert("Enter doc_id and question.");
      return;
    }
    document.getElementById("qaResult").innerHTML = "Asking AI...";
    try {
      const res = await fetch("http://localhost:5000/api/v1/qa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_id: docId, query })
      });
      const j = await res.json();
      if (res.ok) {
        document.getElementById("qaResult").innerHTML = `<pre style="background:#f6f6f6; padding:10px;">${j.answer}</pre>`;
      } else {
        document.getElementById("qaResult").innerHTML = `<div>Error: ${j.error}</div>`;
      }
    } catch (e) {
      document.getElementById("qaResult").innerHTML = `Error: ${e.message}`;
    }
  });
})();
