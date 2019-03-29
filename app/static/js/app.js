function buildLineChart(data) {
    var sixty_day_pred = data.sixty;
    var thirty_day_pred = data.thirty;
    var ten_day_pred = data.ten;
    var actual = data.actual;

    console.log(actual);

    var trace1 = {
        x: Object.keys(actual),
        y: Object.values(actual),
        type: "scatter",
        name: "actual"
    };

    var trace2 = {
        x: Object.keys(sixty_day_pred),
        y: Object.values(sixty_day_pred),
        type: "scatter",
        name: "sixty"
    };

    var d = [trace1, trace2];

    Plotly.newPlot("plot", d);
};

function buildCards(data) {

};

// function init() {
//     // Grab a reference to the input element
//     var selector = d3.select("#ticker-dataset");

//     // Use the list of ticker names to populate the input options
//     d3.json("/ticker").then((tickers) => {
//         tickers.forEach((ticker) => {
//         selector
//             .append("option")
//             .property("value", ticker);
//         });
//     });
// };

function updateDashboard() {
    // Create URL to 
    var url = "/data";
    d3.json(url, function(response) {
        buildLineChart(response);
    });
};

updateDashboard();