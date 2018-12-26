        function EchartObject(name, option = {}){
            let dom = document.getElementById(name);
            dom.style.height = window.innerHeight + 'px';
            var myChart = echarts.init(dom);
            var option = option;
            this.setXAsix = (data) => {
                for(let x of option.xAxis){
                    if(x.type === 'category') {
                        x.data = data
                    }
                }
            }
            this._drawScatter = function (name, data, {
                xAxis = 0,
                yAxis = 0,
                showInLegend = true,
                visualMapIndex = null,
            }) {
                if(showInLegend) {
                    option.legend.data.push(name);
                }
                option.series.push({
                    name: name,
                    type: 'scatter',
                    xAxisIndex: xAxis,
                    yAxisIndex:yAxis,
                    data: data
                });
                if(visualMapIndex != null) {
                    option.visualMap[visualMapIndex].seriesIndex.push(option.series.length - 1)
                }
            }
            this._drawLine = function (name, data,
                                  {xAxis = 0,
                                      yAxis = 0,
                                      showInLegend = true,
                                      step = false,
                                      showSymbol = false,
                                      color = '#333aee',
                                  }) {
                if(showInLegend) {
                    option.legend.data.push(name);
                }
                option.series.push({
                    name: name,
                    type: 'line',
                    xAxisIndex: xAxis,
                    yAxisIndex:yAxis,
                    color: color,
                    showSymbol: showSymbol,
                    step: step,
                    data: data
                });
            }

            this._drawBar = function (name, data, {xAxis = 0,yAxis = 0, showInLegend = true, showSymbol = false, color = '#ee7300', visualMapIndex = null} ) {
                if(showInLegend) {
                    option.legend.data.push(name);
                }
                option.series.push({
                    name: name,
                    type: 'bar',
                    xAxisIndex: xAxis,
                    yAxisIndex:yAxis,
                    color: color,
                    showSymbol: showSymbol,
                    data: data
                });
                if(visualMapIndex) {
                    option.visualMap[visualMapIndex].seriesIndex.push(option.series.length - 1)
                }
            }
            this._drawCandlestick = function (name, data,
                                              {xAxis = 0,
                                                  yAxis = 0,
                                                  showInLegend = true,
                                                  colorP = "#ec0000",
                                                  colorF = '#00da3c',
                                                  borderColorP = null,
                                                  borderColorF = null,
                                              }) {
                option.series.push({
                    name: name,
                    type: 'candlestick',
                    xAxisIndex: xAxis,
                    yAxisIndex: yAxis,
                    itemStyle: {
                        normal: {
                            color: colorP,
                            color0: colorF,
                            borderColor: null,
                            borderColor0: null
                        }
                    },
                    data: data,
                })
            }

            this.draw = ()=>{
                myChart.setOption(option);
            }
    }

    function praser(index) {
        let _index = index;
        return function parseData(arry, _opener,_indexopener){
            function defaultOpener(value, index) {
                return [
                    value
                ]
            }
            function defaultindex(v,k) {
                return _index[k];
            }
            if(!_opener) _opener = defaultOpener;
            if(!_indexopener) _indexopener = defaultindex;
            return arry.map((v,k) =>{
                let index = _indexopener(v,k);
                let index_arr = index == null ? [] : [index,]
                let vals  = index_arr.concat(_opener(v, k));
                return vals
            })
        }
    }

