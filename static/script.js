
const el = document.querySelector('.orange');
const style = getComputedStyle(el);
const color = style.backgroundColor;

const days = window.days;
const turts = window.turts;


const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'line', // bar, pie, doughnut, radar, etc.
  data: {
    labels: days,
    datasets: [{
      label: 'Total Number of Turts Gained/Lost',
      data: turts,
      borderWidth: 6,
      borderColor: color,
      backgroundColor: color,
      tension: 0.1
    }]
  },
  options: {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      labels: {
        color:  '#003366',
        font: {
          family: "sans-serif",
          size: 14,
          weight: "600"
        }
      }
    },
    title: {
      display: true,
      text: "Total Turts Over Time",
      color: '#003366',
      font: {
        family: "sans-serif",
        size: 30,
        weight: "700"
      },
      padding: 20
    }
  },

  scales: {
    x: {
      ticks: {
        color: '#003366' ,
        font: {
          family: "sans-serif",
          size: 14,
          weight: "500"
        },
        maxRotation: 45,
        minRotation: 45
      },
      grid: {
        color: "rgba(0,0,0,0.1)",
        lineWidth: 1
      },
      title: {
        display: true,
        text: "Day of Week",
        color:  '#003366',
        font: {
          family: "sans-serif",
          size: 16,
          weight: "600"
        }
      }
    },

    y: {
      ticks: {
        color:  '#003366',
        font: {
          family: "sans-serif",
          size: 14,
          weight: "500"
        }
      },
      grid: {
        color: "rgba(0,0,0,0.1)",
        lineWidth: 1
      },
      title: {
        display: true,
        text: "Turts",
        color:  '#003366',
        font: {
          family: "sans-serif",
          size: 16,
          weight: "600"
        }
      }
    }
  }
}

});

