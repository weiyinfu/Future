手写K线图
<template>
  <div class="Hand">
    <div v-if="kline.x" class="kline">
      <div v-for="(i,ind) in visibleGrid" :key="ind" class="bar" :title="i.content">
        <div :style="i.up" class="line"></div>
        <div :style="i.middle" class="middle"></div>
        <div :style="i.down" class="line"></div>
      </div>
    </div>
    <div class="operationBlock">
      <el-slider v-model="range" range show-stops :max="gridStyle.length"></el-slider>
    </div>
  </div>
</template>
<script>
import { getUrl } from "../js/net.ts";

const axios = require("axios");
export default {
  data() {
    return {
      kline: {},
      gridStyle: [],
      range: [0, 100]
    };
  },
  computed: {
    visibleGrid() {
      return this.gridStyle.slice(this.range[0], this.range[1]);
    }
  },
  mounted() {
    window.haha = this;
    document.title = "手写K线图";
    axios.get(getUrl("/api/get_data")).then(resp => {
      this.kline = resp.data;
      let max = 0,
        min = 1e9;
      this.range[1] = this.kline.y.length;
      const n = this.kline.y.length;
      for (let i = 0; i < n; i++) {
        max = Math.max(max, this.kline.y[i][3]);
        min = Math.min(min, this.kline.y[i][2]);
      }
      const M = max - min;
      function get(h) {
        return (h / M) * 100 + "%";
      }
      function getTop(h) {
        return ((max - h) / M) * 100 + "%";
      }
      for (let i = 0; i < n; i++) {
        const [open, close, low, high] = this.kline.y[i];
        const background = open > close ? "red" : "green";
        const ma = Math.max(open, close),
          mi = Math.min(open, close);
        this.gridStyle.push({
          day: i,
          content: `开盘价:${open},
收盘价:${close},
最高价:${high},
最低价:${low},
            `,
          up: {
            height: get(high - ma),
            top: getTop(high),
            background
          },
          middle: {
            height: get(ma - mi),
            top: getTop(ma),
            background
          },
          down: {
            height: get(mi - low),
            top: getTop(mi),
            background
          }
        });
      }
    });
  },
  methods: {}
};
</script>
<style lang="less">
@import url("../common.less");
@bottom-height: 60px;
.Hand {
  width: 100%;
  height: 100%;
  .kline {
    height: calc(~"100% - " @bottom-height);
    width: 100%;
    display: flex;
    flex-direction: row;
  }
  .operationBlock {
    height: @bottom-height;
    width: 100%;
    .el-slider {
      padding: 20px;
    }
  }
  .bar {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    .middle {
      background: red;
      position: absolute;
      width: 100%;
    }
    .line {
      position: absolute;
      width: 50%;
    }
  }
  & > div {
    background: black;
  }
}
</style>