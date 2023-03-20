<template>
  <div id="chart">
    <!--
        <div class="toolbar">
          <q-btn id="one_month"
              @click="updateData('one_month')" :class="{active: selection==='one_month'}"
              >
            1M
          </q-btn>

          <button id="six_months"
              @click="updateData('six_months')" :class="{active: selection==='six_months'}"
              >
            6M
          </button>

          <button id="one_year"

              @click="updateData('one_year')" :class="{active: selection==='one_year'}"
              >
            1Y
          </button>

          <button id="ytd"
              @click="updateData('ytd')" :class="{active: selection==='ytd'}"
              >
            YTD
          </button>

          <button id="all"
              @click="updateData('all')" :class="{active: selection==='all'}"
              >
            ALL
          </button>
        </div>
    -->

    <div id="chart-timeline">
      <apexchart
        type="bar"
        height="350"
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
        chart: {
          background: '#0000',
          foreColor: '#fff',
          id: 'area-datetime',
          type: 'bar',
          height: 350,
          zoom: {
            autoScaleYaxis: true
          }
        },
        theme: {
          mode: 'dark',
          palette: 'palette2'
        },
        dataLabels: {
          enabled: false
        },
        markers: {
          size: 0,
          style: 'hollow'
        },
        xaxis: {
          type: 'datetime',
          // min: new Date('01 Mar 2012').getTime(),
          tickAmount: 6
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
