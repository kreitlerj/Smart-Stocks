function buildPredictionChart(data) {
    var prices = Object.values(data);
    var dates = Object.keys(data);

    dates.forEach(function(part, index) {
        dates[index] = new Date(parseInt(part)).toISOString().split('T')[0]
    })
    var actual = []
    var sixty_day = []
    var thirty_day = []
    var ten_day = []

    prices.forEach(function(element) {
        actual.push(element.close);
        sixty_day.push(element.sixty);
        thirty_day.push(element.thirty);
        ten_day.push(element.ten);
    })

    var trace1 = {
        x: dates,
        y: actual,
        type: "scatter",
        name: "Actual"
    };

    var trace2 = {
        x: dates,
        y: sixty_day,
        type: "scatter",
        name: "Pred 60d"
    };

    var trace3 = {
        x: dates,
        y: thirty_day,
        type: "scatter",
        name: "Pred 30d"
    };

    // var trace4 = {
    //     x: dates,
    //     y: ten_day,
    //     type: "scatter",
    //     name: "ten"
    // };

    var d = [trace1, trace2, trace3];
    var layout = {
        paper_bgcolor:"#222",
        plot_bgcolor: "#222",
        font: {
            color: "white"
        }
    }
    Plotly.newPlot("plot", d, layout);
    
};

function inputChanged(ticker) {
    updateDashboard(ticker)
}

function buildStockChart(data) {

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

function updateDashboard(stock) {
    // Create URL to 
    var url = "/data/" + stock;
    d3.json(url, function(error, response) {
        console.log(response)
        buildPredictionChart(response);
    });
};

function init() {
    updateDashboard("AAPL")
};

init();