<template>
  <div id="chart">
    <div id="chart-timeline">
      <apexchart
        type="bar"
        height="500"
        ref="chart"
        :options="chartOptions"
        :series="series"
      ></apexchart>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'

export default {
  el: '#app',
  components: {
    apexchart: VueApexCharts
  },
  props: {
    views: {
      type: Object
    },
    labels: {
      type: Boolean
    }
  },
  data: function () {
    return {
      series: [
        {
          name: 'Views',
          data: this.views
        }
      ],
      chartOptions: {
        plotOptions: {
          bar: {
            dataLabels: {
              orientation: 'vertical',
              position: 'bottom' // bottom/center/top
            }
          }
        },
        chart: {
          background: '#0000',
          foreColor: '#fff',
          id: 'area-datetime',
          type: 'bar',
          zoom: {
            autoScaleYaxis: true
          }
        },
        dataLabels: {
          enabled: this.labels,
          style: {
            colors: ['#fff']
          },
          offsetY: 10 // play with this value
        },
        yaxis: [
          {
            seriesName: 'Views',
            logarithmic: false,
            tickAmount: 7
          }
        ],
        theme: {
          mode: 'dark',
          palette: 'palette2'
        },
        markers: {
          size: 0,
          style: 'hollow'
        },
        xaxis: {
          type: 'datetime',
          tickAmount: 5
        },
        fill: {
          colorFrom: '#00f',
          type: 'gradient',
          gradient: {
            gradientToColors: ['#f0f'],
            inverseColors: true,
            shadeIntensity: 1,
            opacityFrom: 1,
            opacityTo: 0.9,
            stops: [0, 90, 100]
          }
        }
      },
      selection: 'one_year'
    }
  },
  methods: {
    // updateData: function (timeline) {
    //   this.selection = timeline
    //   this.$refs.chart.zoomX(
    //     new Date('28 Jan 2013').getTime(),
    //     new Date('27 Feb 2013').getTime()
    //   )
    // }

    //   switch (timeline) {
    //     case 'one_month':
    //       break
    //     case 'six_months':
    //       this.$refs.chart.zoomX(
    //         new Date('27 Sep 2012').getTime(),
    //         new Date('27 Feb 2013').getTime()
    //       )
    //       break
    //     case 'one_year':
    //       this.$refs.chart.zoomX(
    //         new Date('27 Feb 2012').getTime(),
    //         new Date('27 Feb 2013').getTime()
    //       )
    //       break
    //     case 'ytd':
    //       this.$refs.chart.zoomX(
    //         new Date('01 Jan 2013').getTime(),
    //         new Date('27 Feb 2013').getTime()
    //       )
    //       break
    //     case 'all':
    //       this.$refs.chart.zoomX(
    //         new Date('23 Jan 2012').getTime(),
    //         new Date('27 Feb 2013').getTime()
    //       )
    //       break
    //     default:
    //   }
    // }
  }
}
</script>
