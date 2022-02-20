console.log("charts loaded");

var pie = new Chart("pie", {
    type: "doughnut",
    data: data,
    options: {
        responsive: true,
        maintainAspectRatio: true,
        title: {
            display: true,
            text: 'Your Spending',
            fontStyle: 'bold',
            fontSize: 20
        },


        tooltips: {
            callbacks: {
                // this callback is used to create the tooltip label
                label: function(tooltipItem, data) {
                    // get the data label and data value to display
                    // convert the data value to local string so it uses a comma seperated number
                    var dataLabel = data.labels[tooltipItem.index];
                    var value = ': $' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].toLocaleString();

                    // make this isn't a multi-line label (e.g. [["label 1 - line 1, "line 2, ], [etc...]])
                    if (Chart.helpers.isArray(dataLabel)) {
                        // show value on first line of multiline label
                        // need to clone because we are changing the value
                        dataLabel = dataLabel.slice();
                        dataLabel[0] += value;
                    } else {
                        dataLabel += value;
                    }

                    // return the text to display on the tooltip
                    return dataLabel;
                }
            }
        }
    }
});

var line_chart = new Chart("line_graph1", {
    type: "line",
    data: data1,
    options: {
        responsive: true,
        maintainAspectRatio: true,
        title: {
            display: true,
            text: 'Your Account Balance',
            fontStyle: 'bold',
            fontSize: 20
        },
    }
});

var line_chart = new Chart("line_graph2", {
    type: "line",
    data: data2,
    options: {
        responsive: true,
        maintainAspectRatio: true,
        title: {
            display: true,
            text: 'Your Withdrawals',
            fontStyle: 'bold',
            fontSize: 20
        },
    }
});

var line_chart = new Chart("line_graph3", {
    type: "line",
    data: data3,
    options: {
        responsive: true,
        maintainAspectRatio: true,
        title: {
            display: true,
            text: 'Your Deposits',
            fontStyle: 'bold',
            fontSize: 20
        },
    }
});
