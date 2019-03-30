function buildPredictionChart(data) {
    var prices = Object.values(data);
    var dates = Object.keys(data);

    dates.forEach(function(part, index) {
        dates[index] = new Date(parseInt(part)).toISOString().split('T')[0];
    });

    var actual = [];
    var sixty_day = [];
    var thirty_day = [];
    var ten_day = [];

    prices.forEach(function(element) {
        actual.push(element.close);
        sixty_day.push(element.sixty);
        thirty_day.push(element.thirty);
        ten_day.push(element.ten);
    });

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
        title: "Close Predictions",
        paper_bgcolor:"#222",
        plot_bgcolor: "#222",
        font: {
            color: "white"
        },
        xaxis: {
            rangeslider: {
                visible: true
            }
        }
    };

    Plotly.newPlot("pred-plot", d, layout);
    
};

function inputChanged(ticker) {
    updateDashboard(ticker);
};

function buildStockChart(data) {
    var prices = Object.values(data);
    var dates = Object.keys(data);

    dates.forEach(function(part, index) {
        dates[index] = new Date(parseInt(part)).toISOString().split('T')[0];
    });

    var open = [];
    var close = [];
    var high = [];
    var low = [];

    prices.forEach(function(element) {
        open.push(element.open);
        close.push(element.close);
        high.push(element.high);
        low.push(element.low);
    });

    var trace = {
        x: dates,
        close: close,
        high: high,
        low: low,
        open: open,
      
        // cutomise colors
        increasing: {line: {color: 'black'}},
        decreasing: {line: {color: 'red'}},
      
        type: 'candlestick'
    };
    
    var d = [trace];

    var layout = {
        title: "Candlestick Chart",
        paper_bgcolor:"#222",
        plot_bgcolor: "#222",
        font: {
            color: "white"
        },
    };

    Plotly.newPlot("candlestick-plot", d, layout);
};

function buildPredCards(predictions, errors) {
    var pred = predictions;
    var error = errors;

    var sixty_pred_error = [{'pred': pred.sixty, 'err': error.sixty}];
    var thirty_pred_error = [{'pred': pred.thirty, 'err': error.thirty}];
    var ten_pred_error = [{'pred': pred.ten, 'err': error.ten}];

    d3.select("#sixty_p")
        .selectAll("p")
        .data(sixty_pred_error)
        .enter()
        .append("p")
        .text(function(d) {
            return "Prediction: " + String(sixty_pred_error.pred);
        });
    
        d3.select("#sixty_e")
        .selectAll("p")
        .data(sixty_pred_error)
        .enter()
        .append("p")
        .text(function(d) {
            return "Mean Error: " + String(sixty_pred_error.err);
        });

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
    // Create URL to grab data from the flask app
    var url = "/data/" + stock;
    d3.json(url, function(error, response) {
        console.log(response);
        buildPredictionChart(response);
        buildStockChart(response);
        //buildPredCards(response.predictions, response.error);
    });

};

function init() {
    updateDashboard("AAPL")
};

init();