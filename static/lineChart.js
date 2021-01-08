const lineCtx = document.getElementById('line-chart').getContext('2d');

const getRandomRGB = () => {
  r = Math.floor(Math.random() * 200) + 40;
  g = Math.floor(Math.random() * 200) + 40;
  b = Math.floor(Math.random() * 200) + 40;

  return `rgb(${r}, ${g}, ${b})`;
};

// Fetches
const fetchProductData = async () => {
  const res = await fetch('/ebay_price_tracker/api/products');
  const data = await res.json();
  return data;
};

const fetchPriceData = async () => {
  const res = await fetch('/ebay_price_tracker/api/prices');
  const data = await res.json();
  return data;
};

const fetchDateData = async () => {
  const res = await fetch('/ebay_price_tracker/api/dates');
  const data = await res.json();
  return data;
};

// ----------------------------------------------
// Functions to build chart data
// ----------------------------------------------
const buildChartLabels = dateData => {
  const labels = [];
  for (let i = 0; i < dateData.length; i++) {
    labels.push(dateData[i]['date']);
  }
  return labels;
};

// function for buildDatasets() --------------------------->
const buildDatasetsData = async (dateData, productId) => {
  const res = await fetch('/ebay_price_tracker/api/prices/' + productId);
  const priceDataById = await res.json();

  datasetsData = [];

  for (let i = 0; i < dateData.length; i++) {
    if (priceDataById[0]) {
      if (dateData[i]['date'] === priceDataById[0]['scraped_date']) break;
      else datasetsData.push(undefined);
    }
  }

  for (let i = 0; i < priceDataById.length; i++) {
    datasetsData.push(priceDataById[i]['price'].replace(/[^0-9.-]+/g, ''));
  }
  return datasetsData;
};
// <---------------------------------------------------------

const buildDatasets = async (productData, dateData) => {
  const datasets = [];

  for (let i = 0; i < productData.length; i++) {
    const productId = productData[i]['id'];
    const data = await buildDatasetsData(dateData, productId);
    const config = {
      data,
      label: productData[i]['name'],
      borderColor: getRandomRGB(),
      fill: false,
    };
    datasets.push(config);
  }

  return datasets;
};

// put them together
const buildChartData = async () => {
  const productData = await fetchProductData();
  const dateData = await fetchDateData();

  const labels = buildChartLabels(dateData);
  const datasets = await buildDatasets(productData, dateData);

  return { labels, datasets };
};

// {
//   labels: [],
//   datasets: [
//     {
//       data: [],
//       label: '1',
//       borderColor: "",
//       fill: false
//     },
//   ]
// }

const initChart = async () => {
  const data = await buildChartData();

  const myChart = new Chart(lineCtx, {
    type: 'line',
    data,
    options: {
      title: {
        display: true,
        text: 'Product Prices (eBay)',
      },
    },
  });
};

initChart();
