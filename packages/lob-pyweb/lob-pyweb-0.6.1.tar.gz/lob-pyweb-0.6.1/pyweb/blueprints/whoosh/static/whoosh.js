const whoosh = {

    render: function (column) {
        if (column === "path") {
            return function (data, type, row, meta) {
                return '<a href="' + data + '">' + row["title"] + '</a>';
            }
        } else {
            return function (data, type, row, meta) {
                return data;
            }
        }
    },

    initColumns: function (columns) {
        var cols = [];

        $.each(columns, function (i, val) {
            cols.push({"data": val, "render": whoosh.render(val), "defaultContent": "", "title": val});
        });

        return cols;
    },

    table: function (dom, frame) {

        return $(dom).dataTable({
            data: frame.data,
            columns: whoosh.initColumns(["group", "path", "content"], whoosh.render),
            scrollX: false,
            pagingType: "full_numbers",
            columnDefs: [
                {
                    "targets": [2],
                    "visible": false,
                    "searchable": true
                }
            ]
        })
    }

}