$(document).ready(function() {
    $('#inventory').DataTable( {
        ajax: {
            url: 'http://127.0.0.1:5000/getAllItems',
            dataSrc: 'data.items',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [
            { data: 'id' },
            { data: 'name' },
            { data: 'description' },
            { data: 'donorname' },
            { data: 'donoradd' },
            { data: 'contactno' },
            { data: 'category' },
            { data: 'quantity' },
            { data: 'requiredelivery' },
            { data: 'region' },
            { data: 'timesubmitted' }, 
            { data: 'itemstatus' }
        ],
        // responsive: true,
        fixedHeader: true,
        // "scrollX": true,
        // scrollY: 200,
        // deferRender: true,
        // scroller: true, 
    });

    $('#requests').DataTable( {
        ajax: {
            url: 'http://127.0.0.1:5000/getAllRequests',
            dataSrc: 'data.items',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [
            { data: 'reqid' },
            { data: 'requestor' },
            { data: 'deliverylocation' },
            { data: 'itemcategory' },
            { data: 'requestqty' },
            { data: 'timesubmitted' }
        ],
        // responsive: true,
        fixedHeader: true,
        // "scrollX": true,
        // scrollY: 200,
        // deferRender: true,
        // scroller: true, 
    });

    $('#wishlist').DataTable( {
        ajax: {
            url: 'http://127.0.0.1:5000/getWishlist',
            dataSrc: 'data.items',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [
            { data: 'id' },
            { data: 'itemName' },
            { data: 'remarks' },
            { data: 'category' },
            { data: 'timeSubmitted' },
            { data: 'itemStatus' }
        ],
        // responsive: true,
        fixedHeader: true,
        // "scrollX": true,
        // scrollY: 200,
        // deferRender: true,
        // scroller: true, 
    });


    $('#example').DataTable( {
        // responsive: true,
        fixedHeader: true,
        // "scrollX": true,
        // scrollY: 200,
        // deferRender: true,
        // scroller: true, 
    });

} );    
