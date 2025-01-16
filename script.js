document.getElementById("upload-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const input = document.getElementById("audio-input");
  const resultDiv = document.getElementById("result");

  if (input.files.length === 0) {
    resultDiv.textContent = "Please select an audio file.";
    resultDiv.style.color = "red";
    return;
  }

  resultDiv.textContent = "Processing...";

  const formData = new FormData();
  formData.append("audio", input.files[0]);

  try {
    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    if (response.ok) {
      resultDiv.textContent = `Result: ${result.text}`;
      resultDiv.style.color = "#28a745";
    } else {
      resultDiv.textContent = `Error: ${result.error}`;
      resultDiv.style.color = "red";
    }
  } catch (err) {
    resultDiv.textContent = "An error occurred while processing.";
    resultDiv.style.color = "red";
  }
});