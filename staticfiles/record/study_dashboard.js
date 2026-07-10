document.addEventListener('DOMContentLoaded', function () {
  const labels = JSON.parse(document.getElementById('subject-labels').textContent);
  const data = JSON.parse(document.getElementById('subject-data').textContent);
  const ctx = document.getElementById('subjectChart').getContext('2d');
  const colors = generateColors(data.length);

   new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
});

function generateColors(count) {
  const colors = [];
  for (let i = 0; i < count; i++) {
    const hue = Math.round((360 / count) * i);
    colors.push(`hsl(${hue}, 80%, 70%)`);
  }
  return colors;
}

document.addEventListener('DOMContentLoaded', function() {
  const params = new URLSearchParams(window.location.search);
  if (params.has('period')) {
    const section = document.getElementById('chart-section');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
});
