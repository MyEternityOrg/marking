$('.clickable-row_unp').css('cursor', 'pointer');
$(".clickable-row_unp").click(function () {
    let _url = $(this).data("href");
    $("#ModalWindow").modal("show");
    $.ajax({
        url: _url,
        type: 'get',
        data: {},
        success: function (data) {
            $("#ModalWindow .modal-content").html(data);
        }
    })
})