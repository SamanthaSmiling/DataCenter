document.addEventListener('DOMContentLoaded', function () {


    // Real-time Sales Progress - 水平条形图
    fetch('/api/sales_progress')
        .then(response => response.json())
        .then(data => {
            var ctx = document.getElementById('salesProgressChart').getContext('2d');
            
            let totalSales = data.total_sales;
            let targetSales = data.target_sales;

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Sales Progress'],  // 只显示一个进度条
                    datasets: [
                        {
                            label: 'Total Sales',
                            data: [totalSales],  // 实际销售额
                            backgroundColor: '#4CAF50'
                        },
                        {
                            label: 'Target Sales',
                            data: [targetSales],  // 目标销售额
                            backgroundColor: '#FFC107'
                        }
                    ]
                },
                options: {
                    indexAxis: 'y',  // 水平显示
                    scales: {
                        x: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    }
                }
            });
        });


    

    // 省销量前 10 名
    fetch('/api/provincial_sales_top10')
        .then(response => response.json())
        .then(data => {
            var ctx = document.getElementById('provincialSalesChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.provinces,
                    datasets: [{
                        label: 'Sales',
                        data: data.sales,
                        backgroundColor: '#4CAF50'
                    }]
                }
            });
        });

    // 低库存报警
    fetch('/api/low_stock_alert')
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById('lowStockTable');
            tableBody.innerHTML = '';
            data.products.forEach((product, index) => {
                let row = `<tr>
                            <td>${product}</td>
                            <td>${data.stocks[index]}</td>
                           </tr>`;
                tableBody.innerHTML += row;
            });
        });

    // 异常门店
    fetch('/api/abnormal_sales_stores')
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById('abnormalSalesTable');
            tableBody.innerHTML = '';
            data.stores.forEach((store, index) => {
                let row = `<tr>
                            <td>${store}</td>
                            <td>${data.health_scores[index]}</td>
                           </tr>`;
                tableBody.innerHTML += row;
            });
        });

    // 成交类目结构
    fetch('/api/category_structure')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById('categoryChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.categories,
                datasets: [{
                    data: data.sales,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
                }]
            }
        });
    });
    // 进度缺口诊断
    fetch('/api/progress_gap')
        .then(response => response.json())
        .then(data => {
            var ctx = document.getElementById('progressGapChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.provinces,
                    datasets: [{
                        label: 'Progress Gap',
                        data: data.progress,
                        backgroundColor: data.colors
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
    // 贷款额度池消耗比例
    fetch('/api/loan_pool')
        .then(response => response.json())
        .then(data => {
            var ctx = document.getElementById('loanPoolChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Used', 'Available'],
                    datasets: [{
                        data: [data.loan_pool_usage, 100 - data.loan_pool_usage],
                        backgroundColor: ['#4CAF50', '#FFCE56']
                    }]
                }
            });
        });
    // 系统负荷指数
    fetch('/api/system_load')
        .then(response => response.json())
        .then(data => {
            var ctx = document.getElementById('systemLoadChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Load', 'Available'],
                    datasets: [{
                        data: [data.system_load, 100 - data.system_load],
                        backgroundColor: ['#FFCE56', '#36A2EB']
                    }]
                }
            });
        });
    // 在仓商品的销售进度
    fetch('/api/stock_sales_progress')
        .then(response => response.json())
        .then(data => {
            var ctx = document.getElementById('stockSalesChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Sold', 'In Stock'],
                    datasets: [{
                        data: [data.stock_sales_progress, 100 - data.stock_sales_progress],
                        backgroundColor: ['#FF6384', '#FFCE56']
                    }]
                }
            });
        });

// 商品结构分布图数据逻辑
fetch('/api/product-structure')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById('productStructureChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.categories,
                datasets: [{
                    data: data.sales,
                    backgroundColor: ['#4CAF50', '#FFC107', '#FF6384', '#36A2EB', '#FFCE56'],
                }]
            },
            options: {
                responsive: true,
            }
        });
    })
    .catch(error => console.error('Error fetching product structure data:', error));

// 分类目的近30天成交趋势图数据逻辑
fetch('/api/category-trends')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById('categoryTrendsChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.dates,
                datasets: data.trends.map((trend, index) => ({
                    label: trend.category,
                    data: trend.sales,
                    borderColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'][index % 5],
                    fill: false
                }))
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Sales'
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching category trends data:', error));

// 商品表格数据逻辑
fetch('/api/product-table')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('productTableBody');
        tbody.innerHTML = '';  // 清空表格
        data.forEach(product => {
            const row = `
                <tr>
                    <td>${product.name}</td>
                    <td>${product.category}</td>
                    <td>${product.brand}</td>
                    <td>${product.stock}</td>
                    <td>${product.sales30}</td>
                    <td>${product.sales90}</td>
                    <td>${product.isHot ? 'Yes' : 'No'}</td>
                </tr>`;
            tbody.innerHTML += row;
        });
    })
    .catch(error => console.error('Error fetching product table data:', error));


// 省域成交占比堆积图
    if (document.getElementById('provincialTransactionShareChart')) {
        fetch('/api/provincial-transaction-share')
            .then(response => response.json())
            .then(data => {
                var ctx = document.getElementById('provincialTransactionShareChart').getContext('2d');

                // 处理数据，每年一组数据，每组显示各省份的占比
                const datasets = data.years.map((year, index) => ({
                    label: year,
                    data: data.transactions[year],
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'][index % 4],  // 使用不同颜色
                    stack: 'Stack 0'  // 将不同年份的数据堆积
                }));

                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.provinces,  // 省份名称
                        datasets: datasets
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(tooltipItem) {
                                        const value = tooltipItem.raw;
                                        return ` ${(value * 100).toFixed(2)}%`;  // 显示百分比
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                stacked: true,  // 各年份的数据堆积在一起
                            },
                            y: {
                                stacked: false,  // 不累积年份，单独显示每个年份的占比
                                ticks: {
                                    beginAtZero: true,
                                    callback: function(value) {
                                        return value * 100 + '%';  // 将Y轴刻度显示为百分比
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching provincial transaction share data:', error));
    }

    // Top 3 & Bottom 3 省份的成交趋势图
    if (document.getElementById('topBottomProvincesTrendsChart')) {
        fetch('/api/top-bottom-provinces-trends')
            .then(response => response.json())
            .then(data => {
                var ctx = document.getElementById('topBottomProvincesTrendsChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.dates,
                        datasets: [
                            ...data.top_provinces.map((province, index) => ({
                                label: province.province,
                                data: province.sales,
                                borderColor: '#4CAF50',
                                fill: false
                            })),
                            ...data.bottom_provinces.map((province, index) => ({
                                label: province.province,
                                data: province.sales,
                                borderColor: '#FF6384',
                                fill: false
                            }))
                        ]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                display: true,
                                title: {
                                    display: true,
                                    text: 'Date'
                                }
                            },
                            y: {
                                display: true,
                                title: {
                                    display: true,
                                    text: 'Sales'
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching top/bottom provinces trends data:', error));
    }

    // 省域成交表格数据
    if (document.getElementById('provincialTransactionTableBody')) {
        fetch('/api/provincial-transaction-table')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('provincialTransactionTableBody');
                tbody.innerHTML = '';  // 清空表格
                data.forEach(province => {
                    const row = `
                        <tr>
                            <td>${province.province}</td>
                            <td>${province.stores}</td>
                            <td>${province.quantity}</td>
                            <td>${province.amount}</td>
                            <td>${province.brands}</td>
                            <td>${province.avg_price}</td>
                        </tr>`;
                    tbody.innerHTML += row;
                });
            })
            .catch(error => console.error('Error fetching provincial transaction table data:', error));
    }
    // 门店分层占比饼图
    if (document.getElementById('storeTierDistributionChart')) {
        fetch('/api/store-tier-distribution')
            .then(response => response.json())
            .then(data => {
                var ctx = document.getElementById('storeTierDistributionChart').getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.tiers,
                        datasets: [{
                            data: data.percentages,
                            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
                        }]
                    },
                    options: {
                        responsive: true
                    }
                });
            })
            .catch(error => console.error('Error fetching store tier distribution data:', error));
    }

    // 各城市门店健康评分柱形图
    if (document.getElementById('cityHealthScoresChart')) {
        fetch('/api/city-health-scores')
            .then(response => response.json())
            .then(data => {
                var ctx = document.getElementById('cityHealthScoresChart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.cities,
                        datasets: [{
                            label: 'Health Score',
                            data: data.health_scores,
                            backgroundColor: '#4CAF50'
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching city health scores data:', error));
    }

    // 门店清单表格数据
    if (document.getElementById('storeTableBody')) {
        fetch('/api/store-table')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('storeTableBody');
                tbody.innerHTML = '';  // 清空表格
                data.forEach(store => {
                    const row = `
                        <tr>
                            <td>${store.store_id}</td>
                            <td>${store.transaction_amount}</td>
                            <td>${store.health_score}</td>
                            <td>${store.tier}</td>
                            <td>${store.province}</td>
                            <td>${store.city}</td>
                            <td>${store.owner_id}</td>
                            <td>${store.loan_status ? 'Yes' : 'No'}</td>
                        </tr>`;
                    tbody.innerHTML += row;
                });
            })
            .catch(error => console.error('Error fetching store table data:', error));
    }

        // 按省的销量柱形图（Top 8）
        if (document.getElementById('topProvincesSalesChart')) {
            fetch('/api/top-provinces-sales')
                .then(response => response.json())
                .then(data => {
                    var ctx = document.getElementById('topProvincesSalesChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.provinces,
                            datasets: [{
                                label: 'Sales Amount',
                                data: data.sales,
                                backgroundColor: '#36A2EB'
                            }]
                        },
                        options: {
                            responsive: true,
                            indexAxis: 'y',  // 水平柱形图
                            scales: {
                                x: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                })
                .catch(error => console.error('Error fetching top provinces sales data:', error));
        }
    
        // 分类目成交进度柱形图
        if (document.getElementById('categoryTransactionProgressChart')) {
            fetch('/api/category-transaction-progress')
                .then(response => response.json())
                .then(data => {
                    var ctx = document.getElementById('categoryTransactionProgressChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.categories,
                            datasets: [{
                                label: 'Progress',
                                data: data.progress,
                                backgroundColor: '#4BC0C0'
                            }]
                        },
                        options: {
                            responsive: true,
                            indexAxis: 'y',  // 水平柱形图
                            scales: {
                                x: {
                                    beginAtZero: true,
                                    max: 1  // 进度百分比，最大值为1
                                },
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                })
                .catch(error => console.error('Error fetching category transaction progress data:', error));
        }
    
        // 省域成交表格数据
        if (document.getElementById('provincialTransactionTableBody')) {
            fetch('/api/provincial-transaction-table')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('provincialTransactionTableBody');
                    tbody.innerHTML = '';  // 清空表格
                    data.forEach(province => {
                        const row = `
                            <tr>
                                <td>${province.province}</td>
                                <td>${province.stores}</td>
                                <td>${province.quantity}</td>
                                <td>${province.amount}</td>
                                <td>${province.brands}</td>
                                <td>${province.avg_price}</td>
                            </tr>`;
                        tbody.innerHTML += row;
                    });
                })
                .catch(error => console.error('Error fetching provincial transaction table data:', error));
        }
       // 有无贷款门店的成交占比饼图
       if (document.getElementById('loanSalesDistributionChart')) {
        fetch('/api/loan-sales-distribution')
            .then(response => response.json())
            .then(data => {
                var ctx = document.getElementById('loanSalesDistributionChart').getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.categories,
                        datasets: [{
                            data: data.sales,
                            backgroundColor: ['#4CAF50', '#FF6384']
                        }]
                    },
                    options: {
                        responsive: true
                    }
                });
            })
            .catch(error => console.error('Error fetching loan sales distribution data:', error));
    }

    // 贷款还款率饼图
    if (document.getElementById('loanRepaymentRateChart')) {
        fetch('/api/loan-repayment-rate')
            .then(response => response.json())
            .then(data => {
                var ctx = document.getElementById('loanRepaymentRateChart').getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.categories,
                        datasets: [{
                            data: data.percentages,
                            backgroundColor: ['#36A2EB', '#FFCE56']
                        }]
                    },
                    options: {
                        responsive: true
                    }
                });
            })
            .catch(error => console.error('Error fetching loan repayment rate data:', error));
    }

    // 门店贷款清单表格数据
    if (document.getElementById('loanStoreTableBody')) {
        fetch('/api/loan-store-table')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('loanStoreTableBody');
                tbody.innerHTML = '';  // 清空表格
                data.forEach(store => {
                    const row = `
                        <tr>
                            <td>${store.store_id}</td>
                            <td>${store.city}</td>
                            <td>${store.province}</td>
                            <td>${store.transaction_amount}</td>
                            <td>${store.loan_status ? 'Yes' : 'No'}</td>
                            <td>${store.repayment_status ? 'Yes' : 'No'}</td>
                        </tr>`;
                    tbody.innerHTML += row;
                });
            })
            .catch(error => console.error('Error fetching loan store table data:', error));
    } 
   // 门店明细表格数据
   if (document.getElementById('storeDetailsTableBody')) {
    fetch('/api/store-details')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('storeDetailsTableBody');
            tbody.innerHTML = '';  // 清空表格
            data.forEach(store => {
                const row = `
                    <tr>
                        <td>${store.store_id}</td>
                        <td>${store.transaction_amount}</td>
                        <td>${store.purchase_cost}</td>
                        <td>${store.sales_revenue}</td>
                        <td>${store.promotion_cost}</td>
                        <td>${store.logistics_cost}</td>
                        <td>${store.inventory_depreciation}</td>
                        <td>${store.ebita}</td>
                        <td>${(store.ebita_rate * 100).toFixed(2)}%</td>
                    </tr>`;
                tbody.innerHTML += row;
            });
        })
        .catch(error => console.error('Error fetching store details data:', error));
}

// 省域明细表格数据
if (document.getElementById('provincialDetailsTableBody')) {
    fetch('/api/provincial-details')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('provincialDetailsTableBody');
            tbody.innerHTML = '';  // 清空表格
            data.forEach(province => {
                const row = `
                    <tr>
                        <td>${province.province}</td>
                        <td>${province.transaction_amount}</td>
                        <td>${province.purchase_cost}</td>
                        <td>${province.sales_revenue}</td>
                        <td>${province.promotion_cost}</td>
                        <td>${province.logistics_cost}</td>
                        <td>${province.inventory_depreciation}</td>
                        <td>${province.ebita}</td>
                        <td>${(province.ebita_rate * 100).toFixed(2)}%</td>
                    </tr>`;
                tbody.innerHTML += row;
            });
        })
        .catch(error => console.error('Error fetching provincial details data:', error));
}

// 类目明细表格数据
if (document.getElementById('categoryDetailsTableBody')) {
    fetch('/api/category-details')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('categoryDetailsTableBody');
            tbody.innerHTML = '';  // 清空表格
            data.forEach(category => {
                const row = `
                    <tr>
                        <td>${category.category}</td>
                        <td>${category.transaction_amount}</td>
                        <td>${category.purchase_cost}</td>
                        <td>${category.sales_revenue}</td>
                        <td>${category.promotion_cost}</td>
                        <td>${category.logistics_cost}</td>
                        <td>${category.inventory_depreciation}</td>
                        <td>${category.ebita}</td>
                        <td>${(category.ebita_rate * 100).toFixed(2)}
                    </tr>`;
                tbody.innerHTML += row;
            });
        })
        .catch(error => console.error('Error fetching provincial details data:', error));
}

// 分类库存余量图表
fetch('/api/supply-category-details')
    .then(response => response.json())
    .then(data => {
        var categories = data.map(item => item.product_id);
        var stockRemaining = data.map(item => item.stock_remaining);
        var ctx = document.getElementById('categoryStockChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Stock Remaining',
                    data: stockRemaining,
                    backgroundColor: '#4CAF50'
                }]
            }
        });
    });

// 省份配送进度图表
// 确保 fetch 返回的数据被正确处理
fetch('/api/provincial-delivery-progress')
    .then(response => response.json())
    .then(data => {
        var provinces = data.map(item => item.province);
        var deliveryProgress = data.map(item => item.progress);
        
        var ctx = document.getElementById('provinceDeliveryProgressChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',  // 最新版本只用 'bar'
            data: {
                labels: provinces,
                datasets: [{
                    label: 'Delivery Progress (%)',
                    data: deliveryProgress,
                    backgroundColor: '#FFA726',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',  // 设置为水平条形图
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
        
    })
    .catch(error => console.error('Error:', error));  // 捕获任何错误并输出到控制台








});



Chart.pluginService.register({
    beforeDraw: function(chart) {
        if (chart.config.options.plugins && chart.config.options.plugins.centerText) {
            var width = chart.chart.width,
                height = chart.chart.height,
                ctx = chart.chart.ctx;

            ctx.restore();
            var fontSize = (height / 114).toFixed(2);
            ctx.font = fontSize + "em sans-serif";
            ctx.textBaseline = "middle";

            var text = chart.config.options.plugins.centerText.text,
                textX = Math.round((width - ctx.measureText(text).width) / 2),
                textY = height / 1.5;

            ctx.fillText(text, textX, textY);
            ctx.save();
        }
    }
});
