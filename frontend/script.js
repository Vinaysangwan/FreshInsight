const fileInput = document.getElementById("fileElem");
const preview = document.getElementById("preview");
const result = document.getElementById("result");

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  // 🖼️ Show preview
  const img = document.createElement("img");
  img.src = URL.createObjectURL(file);
  preview.innerHTML = "";
  preview.appendChild(img);

  // ⏳ Show loading state
  result.innerHTML = `<p>🔍 Analyzing image...</p>`;

  try {
    // 📡 Send to backend
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    // ❌ Handle error
    if (data.error) {
      result.innerHTML = `<p style="color:red;">${data.error}</p>`;
      return;
    }

    // ✅ Show result
    result.innerHTML = `
      <h3>Result</h3>
      <p><b>🍎 Name:</b> ${data.name}</p>
      <p><b>🔥 Calories:</b> ${data.calories}</p>
      <p><b>💪 Protein:</b> ${data.protein}</p>
      <p><b>⏳ Freshness:</b> ${data.freshness}</p>
      <p><b>⏳ Confidence:</b> ${data.confidence}</p>
    `;

  } catch (err) {
    console.error(err);
    result.innerHTML = `<p style="color:red;">⚠️ Server error. Try again.</p>`;
  }
});
