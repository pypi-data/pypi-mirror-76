const performance = {
    parse: function (x) {
        rows = [];
        for (var key in x) {
            rows.push({"name": key, "value": x[key]});
        }
        return rows;
    },

    truncate: function (s) {
        var n = s.xData.length;
        var pairs = [];

        for (i = 0; i < n; i++) {
            if (s.xData[i] >= s.xAxis.getExtremes().min && s.xData[i] <= s.xAxis.getExtremes().max) {
                pairs.push([s.xData[i], s.yData[i]])
            }
        }

        return pairs;
    },

    performance: function (s) {
        return $.ajax({
            url: "/engine/performance",
            type: "POST",
            data: JSON.stringify(performance.truncate(s)),
            contentType: "application/json; charset=utf-8"
        });
    },


    monthtable: function (s) {
        return $.ajax({
            url: "/engine/month",
            type: "POST",
            data: JSON.stringify(s),
            contentType: "application/json; charset=utf-8"
        });
    },

    drawdown: function (s) {
        return $.ajax({
            url: "/engine/drawdown",
            type: "POST",
            data: JSON.stringify(s),
            contentType: "application/json; charset=utf-8",
        });
    },

    volatility: function (s) {
        return $.ajax({
            url: "/engine/volatility",
            type: "POST",
            data: JSON.stringify(s),
            contentType: "application/json; charset=utf-8",
        });
    }
};
