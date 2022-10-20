$(document).ready(function () {
    $('#datatable').DataTable({
        "language": {
            "processing": "Подождите...",
            "search": "Поиск:",
            "lengthMenu": "Показать _MENU_ записей",
            "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "infoEmpty": "Записи с 0 до 0 из 0 записей",
            "infoFiltered": "(отфильтровано из _MAX_ записей)",
            "loadingRecords": "Загрузка записей...",
            "zeroRecords": "Записи отсутствуют.",
            "emptyTable": "В таблице отсутствуют данные",
            "paginate": {
                "first": "Первая",
                "previous": "Предыдущая",
                "next": "Следующая",
                "last": "Последняя"
            },
            "aria": {
                "sortAscending": ": активировать для сортировки столбца по возрастанию",
                "sortDescending": ": активировать для сортировки столбца по убыванию"
            },
            "select": {
                "rows": {
                    "_": "Выбрано записей: %d",
                    "1": "Выбрана одна запись"
                },
                "cells": {
                    "_": "Выбрано %d ячеек",
                    "1": "Выбрана 1 ячейка "
                },
                "columns": {
                    "1": "Выбран 1 столбец ",
                    "_": "Выбрано %d столбцов "
                }
            },
        },
        "scrollY": "65vh",
        "scrollCollapse": true,
        "paging": false,
        "searching": false
    });
    $('.dataTables_length').addClass('bs-select');
});