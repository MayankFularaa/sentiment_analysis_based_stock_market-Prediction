const ctx1 = document.getElementById('stockChart').getContext('2d');
const ctx2 = document.getElementById('priceVolumeChart').getContext('2d');
const ctx3 = document.getElementById('smaEmaChart').getContext('2d');
const ctx4 = document.getElementById('sentimentChart').getContext('2d');

let stockChart, priceVolumeChart, smaEmaChart, sentimentChart;

// Utility to format timestamp
function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toISOString().split('T')[0];
}

// Chart export
function exportChart() {
  const link = document.createElement('a');
  link.download = 'stock_prediction_chart.png';
  link.href = stockChart.toBase64Image();
  link.click();
}

// Form submit handler
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const ticker = document.getElementById('ticker').value.toUpperCase();
  const timeFrame = document.getElementById('time_frame').value;

  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('result').innerHTML = '';
  document.getElementById('news-list').innerHTML = '';

  try {
    // Replace this block with your real API call
    const mockData = await fetchMockData(ticker, timeFrame);
    renderCharts(mockData);
    renderResult(ticker, mockData);
    renderNews(mockData.news);
  } catch (err) {
    document.getElementById('result').innerHTML = `<p class="text-red-400">Error: ${err.message}</p>`;
  } finally {
    document.getElementById('loading').classList.add('hidden');
  }
});

// Chart rendering
function renderCharts(data) {
  const labels = data.dates;
  const predicted = data.predicted;
  const actual = data.actual;
  const volume = data.volume;
  const sma = data.sma;
  const ema = data.ema;
  const sentiment = data.sentiment;

  if (stockChart) stockChart.destroy();
  if (priceVolumeChart) priceVolumeChart.destroy();
  if (smaEmaChart) smaEmaChart.destroy();
  if (sentimentChart) sentimentChart.destroy();

  stockChart = new Chart(ctx1, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Actual Price',
          data: actual,
          borderColor: 'rgba(59, 130, 246, 1)',
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          tension: 0.3
        },
        {
          label: 'Predicted Price',
          data: predicted,
          borderColor: 'rgba(34, 197, 94, 1)',
          backgroundColor: 'rgba(34, 197, 94, 0.2)',
          borderDash: [5, 5],
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { ticks: { color: 'white' } },
        y: { ticks: { color: 'white' } }
      },
      plugins: {
        legend: { labels: { color: 'white' } },
        zoom: {
          pan: { enabled: true, mode: 'xy' },
          zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'xy' }
        }
      }
    }
  });

  priceVolumeChart = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          type: 'line',
          label: 'Price',
          data: actual,
          borderColor: '#3b82f6',
          backgroundColor: '#3b82f680',
          yAxisID: 'y'
        },
        {
          type: 'bar',
          label: 'Volume',
          data: volume,
          backgroundColor: '#10b981',
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { ticks: { color: 'white' } },
        y: {
          position: 'left',
          title: { display: true, text: 'Price', color: 'white' },
          ticks: { color: 'white' }
        },
        y1: {
          position: 'right',
          grid: { drawOnChartArea: false },
          title: { display: true, text: 'Volume', color: 'white' },
          ticks: { color: 'white' }
        }
      },
      plugins: {
        legend: { labels: { color: 'white' } }
      }
    }
  });

  smaEmaChart = new Chart(ctx3, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'SMA',
          data: sma,
          borderColor: '#fbbf24',
          tension: 0.3
        },
        {
          label: 'EMA',
          data: ema,
          borderColor: '#f43f5e',
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { ticks: { color: 'white' } },
        y: { ticks: { color: 'white' } }
      },
      plugins: {
        legend: { labels: { color: 'white' } }
      }
    }
  });

  sentimentChart = new Chart(ctx4, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Sentiment Score',
          data: sentiment,
          borderColor: '#818cf8',
          backgroundColor: '#818cf880',
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { ticks: { color: 'white' } },
        y: { ticks: { color: 'white' }, suggestedMin: -1, suggestedMax: 1 }
      },
      plugins: {
        legend: { labels: { color: 'white' } }
      }
    }
  });
}

// Render info summary
function renderResult(ticker, data) {
  document.getElementById('result').innerHTML = `
    <p>🔍 <strong>Ticker:</strong> ${ticker}</p>
    <p>📅 <strong>Data points:</strong> ${data.dates.length}</p>
    <p>🧠 <strong>Prediction model:</strong> LSTM + FinBERT</p>
    <p>📈 <strong>Latest Predicted:</strong> $${data.predicted.at(-1).toFixed(2)}</p>
    <p>📉 <strong>Latest Actual:</strong> $${data.actual.at(-1).toFixed(2)}</p>
  `;
}

// Render news
function renderNews(newsList) {
  const ul = document.getElementById('news-list');
  newsList.forEach(news => {
    const li = document.createElement('li');
    li.innerHTML = `<a href="${news.link}" target="_blank" class="text-blue-400 hover:underline">${news.title}</a>`;
    ul.appendChild(li);
  });
}

// Mock data generator
async function fetchMockData(ticker, timeFrame) {
  await new Promise(res => setTimeout(res, 1000));
  const len = timeFrame === '1d' ? 24 : timeFrame === '1w' ? 7 : 30;
  const dates = Array.from({ length: len }, (_, i) =>
    formatTime(Date.now() - (len - i) * 24 * 60 * 60 * 1000)
  );

  const randomWalk = (base = 100, volatility = 2) =>
    Array.from({ length: len }, (_, i) =>
      base + Math.sin(i / 2) * volatility + Math.random() * volatility
    );

  return {
    dates,
    predicted: randomWalk(100, 3),
    actual: randomWalk(102, 2),
    volume: Array.from({ length: len }, () => Math.floor(1000000 + Math.random() * 500000)),
    sma: randomWalk(101, 1),
    ema: randomWalk(100.5, 1.2),
    sentiment: Array.from({ length: len }, () => (Math.random() * 2 - 1).toFixed(2)),
    news: [
      { title: "Market rallies on strong earnings", link: "https://example.com/news1" },
      { title: "Tech stocks see major boost", link: "https://example.com/news2" },
      { title: "Investors eye upcoming Fed decision", link: "https://example.com/news3" }
    ]
  };
}
