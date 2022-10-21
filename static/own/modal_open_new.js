document.getElementById('new_record').addEventListener('click', function (e) {
        let _url = document.getElementById('datatable').data('href');
        $("#ModalWindow").modal("show");
        $.ajax({
            url: _url,
            type: 'get',
            data: {},
            success: function (data) {
                $("#ModalWindow .modal-content").html(data);
            }
        })
    }
);