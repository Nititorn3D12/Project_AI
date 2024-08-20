

//สร้าง dynamic html table จากข้อมูล JSON ที่ส่งมาจาก Python
function createTable(tableData, tableID) {
    // create table
    var $table = $('<table class="table table-striped">');
    // caption
    $table.append('<caption>MyTable</caption>')
        // thead
        .append('<thead>').children('thead')
        .append('<tr />').children('tr');
    var columns = tableData["columns"];
    for (let i = 0; i < columns.length; i++) {
        $table.append('<th>' + columns[i] + '</th>');
    }
    //tbody
    var $tbody = $table.append('<tbody />').children('tbody');
    var rows = tableData["rows"]; //rows : แถวหลายแถว
    for (let i = 0; i < rows.length; i++) {
        var row = rows[i]; //row : แถวเดียว
        var trow = $tbody.append('<tr/>').children('tr:last');
        for (let j = 0; j < row.length; j++) {
            var cell = row[j]; //cell : คอลัมในแถวปัจจุบัน
            trow.append("<td>" + cell + "</td>");
        }

    }
    
    $(tableID).html($table);

}


function createChart(data, chartType, chartID) {
    console.log(data);
    var cd = data["chart"];
    var x_label = data["columns"][0];
    var y_label = data["columns"][1];


    const chartBackgroundColor = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(201, 203, 207, 0.2)',
        'rgba(255, 0, 0, 0.2)',
        'rgba(0, 255, 0, 0.2)',
        'rgba(0, 0, 255, 0.2)',
      ]
    
    var bgColor = [];
    for (let i = 0; i < cd["labels"].length; i++) {
        bgColor.push(chartBackgroundColor[i%chartBackgroundColor.length]);
    }

    const chartData = {
        labels: cd["labels"],
        datasets: [{
            data: cd["data"],
            backgroundColor: bgColor
        }]
    };


    options = {
        legend: {display: false},
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: x_label
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: y_label
            }
          }],
        }
      };

    var mybarChart = new Chart(chartID, {
        type: chartType,
        data: chartData,
        options: options
    });
}


function addComboBoxData(resultSet,comboBoxID) {
    var comboBox =  $(comboBoxID)
    var rows = resultSet["rows"]; //rows : แถวหลายแถว

    for (let i = 0; i < rows.length; i++) {
        var row = rows[i];
        var item = row[0];

        comboBox.append('<option value="' + item +'">'+item +'</optoin>');
    }
}

function callApiAddDataToCombobox(url,comboBoxID) {
    
    $.ajax({
            url: url,
            method: "GET",
            dataType: 'json',
            success: function (data) {
                addComboBoxData(data,comboBoxID);
            },
            error: function (xhr, ajaxOptions, thrownError) { alert(thrownError); }
        });

}