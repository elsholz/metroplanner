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
          offsetY: 10
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
  }
}
</script>
