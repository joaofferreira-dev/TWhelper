 /*Handles jQuery Database Logic */

var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

function update_assignment (pk, updatedCell) {
    $.ajax({
        url : "http://localhost:8001/teamsapi/"+pk.toString()+"/",
        type: 'PUT',
                    headers:{"X-CSRFToken": $crf_token},
        contentType: 'multipart/form-data; boundary="---------------------------"',
        data: "-----------------------------\r\nContent-Disposition: form-data; name=\"assignment\"\r\n\r\n"+updatedCell.toString()+"\r\n-----------------------------"
    });
}

function sum (arr) {
    var total=0;
    for(var i in arr) { total += arr[i]; }
    return total
}

$(document).ready(function() {

    var col = [
        {"data": "pk"},
        {"data": "toon1.name", "name": "toon1.name"},
        {"data": "toon1.num_zetas", "name": "toon1.num_zetas"},
        {"data": "toon1.speed", "name": "toon1.speed"},
        {"data": "toon2.name", "name": "toon2.name"},
        {"data": "toon2.num_zetas", "name": "toon2.num_zetas"},
        {"data": "toon2.speed", "name": "toon2.speed"},
        {"data": "toon3.name", "name": "toon3.name"},
        {"data": "toon3.num_zetas", "name": "toon3.num_zetas"},
        {"data": "toon3.speed", "name": "toon3.speed"},
        {"data": "toon4.name", "name": "toon4.name"},
        {"data": "toon4.num_zetas", "name": "toon4.num_zetas"},
        {"data": "toon4.speed", "name": "toon4.speed"},
        {"data": "toon5.name", "name": "toon5.name"},
        {"data": "toon5.num_zetas", "name": "toon5.num_zetas"},
        {"data": "toon5.speed", "name": "toon5.speed"},
        {"data": "Totalgp"},
        {"data": "date_posted"},
        {"data": "author"},
        {"data": "author_username", "name": "author_username"},
        {"data": "assignment"},
    ];

    var col2 = [
        {"data": "pk"},
        {"data": "toon1.name", "name": "toon1.name"},
        {"data": "toon1.num_zetas", "name": "toon1.num_zetas"},
        {"data": "toon1.speed", "name": "toon1.speed"},
        {"data": "toon2.name", "name": "toon2.name"},
        {"data": "toon2.num_zetas", "name": "toon2.num_zetas"},
        {"data": "toon2.speed", "name": "toon2.speed"},
        {"data": "toon3.name", "name": "toon3.name"},
        {"data": "toon3.num_zetas", "name": "toon3.num_zetas"},
        {"data": "toon3.speed", "name": "toon3.speed"},
        {"data": "toon4.name", "name": "toon4.name"},
        {"data": "toon4.num_zetas", "name": "toon4.num_zetas"},
        {"data": "toon4.speed", "name": "toon4.speed"},
        {"data": "toon5.name", "name": "toon5.name"},
        {"data": "toon5.num_zetas", "name": "toon5.num_zetas"},
        {"data": "toon5.speed", "name": "toon5.speed"},
        {"data": "Totalgp"},
        {"data": "date_posted"},
        {"data": "author"},
        {"data": "author_username", "name": "author_username"},
        {"data": "assignment"},
        {
            "class":          "remove",
            "orderable":      false,
            "data":           null,
            "defaultContent": ""
        }
    ];

    table = $('#teams').DataTable({

        "ajax": "/teamsapi/?format=datatables",
        "serverSide": true,
        "processing": true,
        "paging": true,
        "columns": col,
        "columnDefs": [{targets:[1,4,7,10,13],className:"truncate2"}],
        createdRow: function(row){
            var td = $(row).find(".truncate2");
            td.attr("title", td.html());
        },
        "dom": "Bflrtip",
        "buttons": [{
            "text":       'Export Excel',
            action: function (e, dt, node, config) {
                $.ajax({
                    "url": "/export/xls/",
                    "data": dt.ajax.params(),
                    "success": function(res, status, xhr) {
                                                //var excelURL = window.URL.createObjectURL(excelData);
                        var tempLink = document.createElement('a');
                        tempLink.href = "/export/xls/";
                        tempLink.setAttribute('download', 'teams.xlsx');
                        tempLink.click();
                    }
                });
            }
        }],
        "rowCallback": function( row, data ) {
            /* This will filter out the teams which have already been assigned*/
            if ( data["assignment"] != "1" ) {
                /*$(row).hide();*/

                $(row).remove();
            }
        }
   });

   table.MakeCellsEditable({
       "onUpdate": myCallbackFunction,
       "inputCss":'my-input-class',
       "columns": [20],
       "allowNulls": {
           "columns": [20],
           "errorClass": 'error'
       },
       "confirmationButton": { // could also be true
           "confirmCss": 'my-confirm-class',
           "cancelCss": 'my-cancel-class'
       },
       "inputTypes": [

           {
               "column":20,
               "type": "list",
               "options":[
                   { "value": "1", "display": "None" },
                   { "value": "2", "display": "T1" },
                   { "value": "3", "display": "T2" },
                   { "value": "4", "display": "T3" },
                   { "value": "5", "display": "T4" },
                   { "value": "6", "display": "T6" },
                   { "value": "7", "display": "T7" },
                   { "value": "8", "display": "T9" },
                   { "value": "9", "display": "T10" }
               ]
           },
       ]
   });

    /*The following are the datatables of assigned teams to each territory*/
    table_T1 = $('#T1').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       "sClass": "longTextClass",
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "2" ) {
               $(row).hide();
           }

       }
    });

    $('#T1 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T1').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T1').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    table_T2 = $('#T2').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       /*"dom": "Bfrtip",*/
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "3" ) {
               $(row).hide();
           }
       }
    });

    $('#T2 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T2').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T2').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    table_T3 = $('#T3').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       /*"dom": "Bfrtip",*/
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "4" ) {
               $(row).hide();
           }
       }
    });

    $('#T3 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T3').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T3').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    table_T4 = $('#T4').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       /*"dom": "Bfrtip",*/
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "5" ) {
               $(row).hide();
           }
       }
    });

    $('#T4 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T4').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T4').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    table_T6 = $('#T6').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       /*"dom": "Bfrtip",*/
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "6" ) {
               $(row).hide();
           }
       }
    });

    $('#T6 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T6').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T6').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    table_T7 = $('#T7').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       /*"dom": "Bfrtip",*/
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "7" ) {
               $(row).hide();
           }
       }
    });

    $('#T7 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T7').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T7').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    table_T9 = $('#T9').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       /*"dom": "Bfrtip",*/
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "8" ) {
               $(row).hide();
           }
       }
    });

    $('#T9 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T9').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T9').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    table_T10 = $('#T10').DataTable({

       "ajax": "/teamsapi/?format=datatables",
       "serverSide": true,
       "columns": col2,
       "columnDefs": [{targets:1,className:"truncate"}],
       createdRow: function(row){
           var td = $(row).find(".truncate");
           td.attr("title", td.html());
       },
       "searching": false,
       "paging": true,
       "info": false,
       /*"dom": "Bfrtip",*/
       "rowCallback": function( row, data ) {
           /* This will filter out the teams which have already been assigned*/
           if ( data["assignment"] != "9" ) {
               $(row).hide();
           }
       }
    });

    $('#T10 tbody').on( 'click', 'tr td.remove', function () {

        var $tr = $(this).closest('tr');
        var data = $('#T10').DataTable().row($tr).data();
        console.log("Remove:" + data.pk);

        update_assignment (data.pk, 1);

        $('#T10').DataTable().ajax.reload();
        $('#teams').DataTable().ajax.reload();

    } );

    $("#list-header").on({
        /* mouse over behaviours*/
        mouseenter: function() {
            $(this).css("background-color", "lightgray");
        },
        mouseleave: function() {
            $(this).css("background-color", "lightblue");
        },
    });

});

function myCallbackFunction (updatedCell, updatedRow, oldValue) {
    /*console.log("The new value for the cell is: " + updatedCell.data());
    console.log("The old value for that cell was: " + oldValue);
    console.log("The values for each cell in that row are: " + updatedRow.data());
    */
    pk = table.rows(updatedRow).data()[0]["pk"];

    update_assignment (pk, updatedCell.data());

    $('#T1').DataTable().ajax.reload();
    $('#T2').DataTable().ajax.reload();
    $('#T3').DataTable().ajax.reload();
    $('#T4').DataTable().ajax.reload();
    $('#T6').DataTable().ajax.reload();
    $('#T7').DataTable().ajax.reload();
    $('#T9').DataTable().ajax.reload();
    $('#T10').DataTable().ajax.reload();

    console.log("Updated row: " + pk);
}


function destroyTable() {
    if ($.fn.DataTable.isDataTable('#teams')) {
        table.destroy();
        table.MakeCellsEditable("destroy");
    }
}
