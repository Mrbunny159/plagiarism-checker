async function checkPlagiarism() {
  const intro = document.getElementById("intro").value;
  const review = document.getElementById("review").value;

  const res = await fetch("/api/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      introduction: intro,
      literature: review
    })
  });

  const data = await res.json();

  document.getElementById("report").innerHTML = `
    <h3>Plagiarism Scan Report</h3>
    <p>Similarity: ${data.similarity}%</p>
    <p>Originality: ${data.originality}%</p>
    <p><b>Status:</b> ${data.status}</p>
  `;
}
