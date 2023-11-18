var yearData = [
    {
      year: "2020", // 年份
      data: [
        // 两个数组是因为有两条线
        [24, 40, 101, 134, 90, 230, 210, 230, 120, 230, 210, 120],
        [40, 64, 191, 324, 290, 330, 310, 213, 180, 200, 180, 79]
      ]
    }
  ];
 
var x_data = [
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
		"123"
      ]

var labelArray = ['A', 'B', 'C', 'D', 'E']; // 自定义的 label 数组
var my_f;
// 折线图1模块制作
(function() {
  
  // 1. 实例化对象
  var myChart = echarts.init(document.querySelector(".line .chart"));
  // 2.指定配置
  var option = {
    // 通过这个color修改两条线的颜色
    color: ["#00f2f1", "#ed3f35"],
    tooltip: {
      trigger: "axis"
    },
    legend: {
      // 如果series 对象有name 值，则 legend可以不用写data
      // 修改图例组件 文字颜色
      textStyle: {
        color: "#4c9bfd"
      },
      // 这个10% 必须加引号
      right: "10%"
    },
    grid: {
      top: "20%",
      left: "3%",
      right: "4%",
      bottom: "3%",
      show: true, // 显示边框
      borderColor: "#012f4a", // 边框颜色
      containLabel: true // 包含刻度文字在内
    },

    xAxis: {
      type: "category",
      boundaryGap: false,
      data: x_data,
      axisTick: {
        show: false // 去除刻度线
      },
      axisLabel: {
        color: "#4c9bfd" // 文本颜色
      },
      axisLine: {
        show: false // 去除轴线
      }
    },
    yAxis: {
      type: "value",
      axisTick: {
        show: false // 去除刻度线
      },
      axisLabel: {
        color: "#4c9bfd" // 文本颜色
      },
      axisLine: {
        show: false // 去除轴线
      },
      splitLine: {
        lineStyle: {
          color: "#012f4a" // 分割线颜色
        }
      }
    },
    series: [
      {
        name: "新增粉丝",
        type: "line",
        // true 可以让我们的折线显示带有弧度
        smooth: true,
        data: yearData[0].data[0]
      },
      {
        name: "新增游客",
        type: "line",
        smooth: true,
        data: yearData[0].data[1],
		label: {
                show: true, // 显示数据标签
                position: 'top', // 数据标签位置，可以是 'top', 'bottom', 'inside', 'insideTop', 'insideBottom', 'insideLeft', 'insideRight', 'insideTopLeft', 'insideTopRight', 'insideBottomLeft', 'insideBottomRight'
                color: '#FF5733', // 数据标签文本颜色
                fontSize: 12, // 数据标签文本大小
                formatter: function(params) {
                    // 自定义数据标签的文本格式
					var dataIndex = params.dataIndex;
                    
                    return labelArray[dataIndex];
                   
                }
            },
      }
    ]
  };

  // 3. 把配置给实例对象
  myChart.setOption(option);
  // 4. 让图表跟随屏幕自动的去适应
  window.addEventListener("resize", function() {
    myChart.resize();
  });

  // 5.点击切换效果
  my_f = function() {
    // alert(1);
    // console.log($(this).index());
    // 点击 a 之后 根据当前a的索引号 找到对应的 yearData的相关对象
    // console.log(yearData[$(this).index()]);
    var obj = yearData[0];
    option.series[0].data = obj.data[0];
    option.series[1].data = obj.data[1];
    // 需要重新渲染
    myChart.setOption(option);

  };
})();



function addToArray() {
    // 获取输入框的值
    const textInput = document.getElementById('textInput').value;

    // 如果输入框不为空，将文本添加到数组中
    if (textInput.trim() !== '') {
        yearData[0].data[0].push(parseInt(textInput));
		x_data.push("13");
        // 清空输入框
        document.getElementById('textInput').value = '';
		console.log(yearData[0].data[0]);
        my_f();
		updateOutput();
    }
}

function minusToArray() {

    yearData[0].data[0].splice(3, 1);
	x_data.splice(3, 1);
	console.log(yearData[0].data[0]);
    my_f();
    updateOutput();
}


function updateOutput() {
    const outputDiv = document.getElementById('output');
    // 清空输出区域
    outputDiv.innerHTML = '';
    
    // 遍历数组并显示在输出区域
    yearData[0].data[0].forEach(function (text, index) {
        const textElement = document.createElement('p');
        textElement.textContent = `文本 ${index + 1}: ${text}`;
        outputDiv.appendChild(textElement);
    });
}