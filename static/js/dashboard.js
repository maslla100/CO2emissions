// JavaScript for interactive visualizations using Plotly

document.addEventListener('DOMContentLoaded', function () {
    // Example data for CO2 emissions over time
    var years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'];
    var emissions = [10000, 12000, 15000, 14000, 13000, 12500, 13500, 14500, 16000, 17000, 18000];  // Example values

    var trace1 = {
        x: years,
        y: emissions,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'CO2 Emissions',
        line: { shape: 'linear', color: '#1f77b4' },
        marker: { size: 8 }
    };

    var data = [trace1];

    var layout = {
        title: 'CO2 Emissions Over Time',
        xaxis: { title: 'Year' },
        yaxis: { title: 'CO2 Emissions (kt)' }
    };

    // Render the chart in a div with id 'co2-chart'
    Plotly.newPlot('co2-chart', data, layout);
});
