$(document).ready(function () {
    $('#dwnldBtn').on('click', function () {
        $("#dataTable").table2excel({
            filename: "employeeData.xls"
        });
    });
});