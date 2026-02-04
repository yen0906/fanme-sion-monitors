async function load() {
  const res = await fetch("/api/data");
  const data = await res.json();
  const tbody = document.getElementById("tbody");
  tbody.innerHTML = "";

  data.forEach((row, i) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${i + 1}</td>
      <td>${row.time}</td>
      <td class="big">-${row.diff}</td>
    `;
    tbody.appendChild(tr);
  });

  document.getElementById("status").innerText =
    "最後更新：" + new Date().toLocaleString();
}

load();
setInterval(load, 5000);
