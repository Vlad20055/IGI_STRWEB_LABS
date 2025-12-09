const xs = [];
for(let i=0;i<=100;i++){
  xs.push(-1.0 + i*(1/100) * 2);
}

function binom2n_n(n){
  if(n===0) return 1;
  let r = 1;
  for(let k=1;k<=n;k++){
    r *= (n + k) / k;
  }
  return r;
}

function a_n(n){
  return binom2n_n(n) / (Math.pow(4,n) * (2*n + 1));
}

function seriesValue(x){
  let s = 0;
  for(let n=0;n<=10;n++){
    s += a_n(n) * Math.pow(x, 2*n + 1);
  }
  return s;
}

const seriesData = xs.map(x => ({x: x, y: seriesValue(x)}));
const exactData  = xs.map(x => ({x: x, y: Math.asin(x)}));

const ctx = document.getElementById('chart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    datasets: [
      {
        label: 'ряд (n=10)',
        data: seriesData,
        borderColor: 'red',
        tension: 0,
        pointRadius: 0,
      },
      {
        label: 'Math.asin(x)',
        data: exactData,
        borderColor: 'blue',
        tension: 0,
        pointRadius: 0,
      }
    ]
  },
  options: {
    responsive: false,
    maintainAspectRatio: true,
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: { display: true, text: 'x' },
        ticks: { stepSize: 0.5 },
        min: -2,
        max: 2
      },
      y: {
        title: { display: true, text: 'y' },
        suggestedMin: -0.6,
        suggestedMax:  0.6
      },
      
    },

    plugins: {
      legend: { display: true },
      annotation: {
        annotations: {
          midLine: {
            type: 'line',
            xMin: 0,
            xMax: 0,
            borderColor: 'green',
            borderWidth: 1,
            label: {
              enabled: true,
              content: 'x=0',
              position: 'start'
            }
          }
        }
      }
    },
    elements: { line: { borderWidth: 2 } },
    responsiveAnimationDuration: 0
  }
});

