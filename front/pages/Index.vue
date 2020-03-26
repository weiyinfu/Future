<template>
    <div class="Index">
        <div class="header">期货行情</div>
        <div class="main">
            <div class="control">
                产品:
                <el-cascader
                        v-model="chosenFuture"
                        :options="productOptions"
                        :props="{ expandTrigger: 'hover' }"
                        @change="handleChange">

                </el-cascader>
                周期:
                <el-select v-model="period" placeholder="请选择" @change="handleChange">
                    <el-option
                            v-for="item in periodOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
                {{future.name}}({{future.code}})
            </div>
            <div ref="finance" class="kline-chart"></div>
        </div>
    </div>
</template>
<script>
    import {getUrl} from "../js/net.ts";

    const echarts = require("echarts");
    /*
    //按需加载的echarts，可以加快渲染速度
    var echarts = require("echarts/lib/echarts");
    // 引入柱状图
    require("echarts/lib/chart/bar");
    require("echarts/lib/chart/pie");
    // 引入提示框和标题组件
    require("echarts/lib/component/tooltip");
    require("echarts/lib/component/title");
    require("echarts/lib/component/visualMap");
    */
    var axios = require("axios");

    function get(x, y, up, down, mid) {
        var upColor = "#ec0000";
        var upBorderColor = "#8A0000";
        var downColor = "#00da3c";
        var downBorderColor = "#008F28";
        return {
            title: {
                text: "K线图",
                left: 0
            },
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    type: "cross"
                }
            },
            legend: {
                data: ["K线", "Up", "Mid", "Down"]
            },
            grid: {
                left: "10%",
                right: "10%",
                bottom: "15%"
            },
            xAxis: {
                type: "category",
                data: x,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: "dataMin",
                max: "dataMax"
            },
            yAxis: {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            dataZoom: [
                {
                    type: "inside",
                    start: 50,
                    end: 100
                },
                {
                    show: true,
                    type: "slider",
                    top: "90%",
                    start: 50,
                    end: 100
                }
            ],
            series: [
                {
                    name: "K线",
                    type: "candlestick",
                    data: y,
                    itemStyle: {
                        color: upColor,
                        color0: downColor,
                        borderColor: upBorderColor,
                        borderColor0: downBorderColor
                    }
                },
                {
                    name: "Up",
                    type: "line",
                    data: up,
                    smooth: true,
                    lineStyle: {
                        opacity: 0.5
                    }
                },
                {
                    name: "Mid",
                    type: "line",
                    data: mid,
                    smooth: true,
                    lineStyle: {
                        opacity: 0.5
                    }
                },
                {
                    name: "Down",
                    type: "line",
                    data: down,
                    smooth: true,
                    lineStyle: {
                        opacity: 0.5
                    }
                }
            ]
        };
    }

    export default {
        data() {
            return {
                kline: null,
                productOptions: [],
                periodOptions: [{
                    label: '5分钟', value: 5 * 60
                }, {
                    label: '10分钟', value: 10 * 60
                }, {
                    label: '半小时', value: 60 * 30,
                }, {
                    label: '1小时', value: 3600
                }, {
                    label: '一天', value: 3600 * 24,
                }],
                chosenFuture: null,
                period: 5 * 60,
                data: {},
            };
        },
        mounted() {
            document.title = "K线图";
            window.haha = this;
            this.kline = echarts.init(this.$refs["finance"]);
            window.onresize = () => {
                this.kline.resize();
            };
            axios.get(getUrl('/api/get_products')).then(resp => {
                const options = resp.data;
                for (let market of options) {
                    market.label = market.name;
                    market.value = market.code;
                    market.children = market.sons;
                    for (let big of market.sons) {
                        big.label = big.name;
                        big.value = big.code;
                        big.children = big.sons;
                        for (let small of big.sons) {
                            small.label = small.name;
                            small.value = small.code;
                        }
                    }
                }
                this.productOptions = options;
                this.chosenFuture = this.getFirstOptions(options);
                this.load();
            })
        },
        computed: {
            future() {
                if (!this.productOptions || !this.chosenFuture) return {
                    name: '', code: ''
                }
                let market = {}
                for (let i of this.productOptions) {
                    if (i.code === this.chosenFuture[0]) {
                        market = i;
                        break;
                    }
                }
                let big = {};
                for (let i of market.sons) {
                    if (i.code === this.chosenFuture[1]) {
                        big = i;
                        break;
                    }
                }
                let small = {};
                for (let i of big.sons) {
                    if (i.code === this.chosenFuture[2]) {
                        small = i;
                        break;
                    }
                }
                return {
                    name: small.name,
                    code: small.code,
                }
            }
        },
        methods: {
            getFirstOptions(options) {
                const a = [];
                let now = options[0];
                while (now) {
                    a.push(now.value);
                    if (!now.children || !now.children.length) break;
                    now = now.children[0];
                }
                return a;
            },
            handleChange() {
                console.log(arguments)
                this.load();
            },
            load() {
                const old_url = "/api/get_data";//mock的数据
                const url = `/api/get_kline?symbol=${this.chosenFuture[2]}&period=${this.period}`
                axios.get(getUrl(url)).then(resp => {
                    const data = resp.data;
                    this.data = data;
                    this.kline.setOption(get(data.x, data.y, data.up, data.down, data.mid));
                });
            }
        }
    };
</script>
<style lang="less">
    @import url("../common.less");

    .Index {
        width: 100%;
        height: 100%;
        @header-height: 40px;
        @header-background-color: #49188a;

        .header {
            height: @header-height;
            background-color: @header-background-color;
            color: white;
            display: flex;
            align-items: center;
            padding: 0 20px;
        }

        .main {
            height: calc(~"100% - " @header-height);
            box-sizing: border-box;

            .control {
                padding: 20px;
            }

            .kline-chart {
                width: 100%;
                height: 500px;
            }
        }
    }
</style>
