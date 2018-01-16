$(document).ready(function() {
    function parseISOLocal(s) {
      var b = s.split(/\D/);
      return new Date(b[0], b[1]-1, b[2], b[3], b[4], b[5]);
    }

    moment.updateLocale('en', {
      week: { dow: 1 }
    });

    $('#datetimepicker2').datetimepicker({
         format: 'DD.MM.YY',
         defaultDate: moment(),
         icons: {
            time: "mdi mdi-av-timer",
            date: "mdi mdi-calendar",
            up: "mdi mdi-chevron-up",
            down: "mdi mdi-chevron-down"
         }
    })
    .on('dp.change', function(e){ refresh_statistic(stream_id, stream_name, e.date.format("X")); });

    refresh_statistic(stream_id, stream_name, moment().format("X"))

    function refresh_statistic(sid, sname, timestamp) {
        $.ajax({
            url: '/api/statistic/'+ sid +'?when='+ timestamp,
            type: 'get',
            success: function (resp, status) {
                $('#no_data').addClass('hide');
                $('.chart').removeClass('hide');
                var data = [];
                for (var prop in resp.checkpoints) {
                    if (resp.checkpoints.hasOwnProperty(prop)) {
                        var point_date = parseISOLocal(resp.checkpoints[prop].created_at)
                        data.push({
                            x: point_date,
                            y: resp.checkpoints[prop].connections,
                            name: resp.checkpoints[prop].song + ' (' + ("0" + point_date.getHours()).slice(-2) + ":" + ("0" + point_date.getMinutes()).slice(-2) + ":" + ("0" + point_date.getSeconds()).slice(-2) + ')'
                        });
                    }
                }

                Highcharts.setOptions({
                    global: {
                        useUTC: false
                    }
                });

                Highcharts.chart(sid, {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: false
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                            'Выделите участок на графике для детализации' : 'Кликните для детализации'
                    },
                    xAxis: {
                        title: {
                            text: 'Шкала времени'
                        },
                        dateTimeLabelFormats: {
                            day: '%e.%m.%Y',
                            hour: '%H:%M %e.%m.%Y',
                            minute: '%H:%M %e.%m.%Y',
                            seconds: '%H:%M:%S %e.%m.%Y'
                        },
                        type: 'datetime'
                    },
                    yAxis: {
                        title: {
                            text: 'Количество слушателей'
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        area: {
                            fillColor: {
                                linearGradient: {
                                    x1: 0,
                                    y1: 0,
                                    x2: 0,
                                    y2: 1
                                },
                                stops: [
                                    [0, Highcharts.getOptions().colors[0]],
                                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                                ]
                            },
                            marker: {
                                radius: 6
                            },
                            lineWidth: 3,
                            states: {
                                hover: {
                                    lineWidth: 1
                                }
                            },
                            threshold: null,
                            turboThreshold: 5800
                        }
                    },
                    series: [{
                        type: 'area',
                        name: sname,
                        data: data
                    }]
                });
            },
            error: function () {
                $('#no_data').removeClass('hide');
                $('.chart').addClass('hide');
            }

        });
    }


});
