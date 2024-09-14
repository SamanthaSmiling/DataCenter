from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# 从 CSV 文件加载
store_data = pd.read_csv('data/store_data.csv')
product_data = pd.read_csv('data/product_data.csv')
transaction_data = pd.read_csv('data/transaction_data.csv')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# 实时成交额进展
@app.route('/api/sales_progress')
def sales_progress():
    total_sales = transaction_data['Amount'].sum()
    target_sales = total_sales * np.random.uniform(0.8, 1.1)  # 随机生成目标值
    return jsonify({
        'total_sales': total_sales,
        'target_sales': target_sales
    })

# 省销量排行榜Top10
@app.route('/api/provincial_sales_top10')
def provincial_sales_top10():
    top_provinces = store_data.groupby('Province')['Sales (Last 3 Months)'].sum().nlargest(10)
    return jsonify({
        'provinces': top_provinces.index.tolist(),
        'sales': top_provinces.values.tolist()
    })

# 成交类目结构
@app.route('/api/category_structure')
def category_structure():
    category_sales = transaction_data.groupby('Category')['Amount'].sum()
    return jsonify({
        'categories': category_sales.index.tolist(),
        'sales': category_sales.values.tolist()
    })
# 进度缺口诊断
@app.route('/api/progress_gap')
def progress_gap():
    province_sales = store_data.groupby('Province')['Sales (Last 3 Months)'].sum()
    province_target = province_sales * np.random.uniform(0.8, 1.1)
    gap = province_target - province_sales
    sorted_gap = gap.nsmallest(8)
    colors = ['#FF5722', '#FF7043', '#FF8A65', '#FFAB91', '#FFCCBC', '#FFE0B2', '#FFF3E0', '#FFFFFF']
    return jsonify({
        'provinces': sorted_gap.index.tolist(),
        'progress': sorted_gap.values.tolist(),
        'colors': colors[:len(sorted_gap)]
    })
# 贷款额度池的消耗比例（固定为35%）
@app.route('/api/loan_pool')
def loan_pool():
    return jsonify({
        'loan_pool_usage': 35  # 固定为 35%
    })
# 系统负荷指数（固定为50%）
@app.route('/api/system_load')
def system_load():
    return jsonify({
        'system_load': 50  # 固定为 50%
    })
# 在仓商品的销售进度（固定为65%）
@app.route('/api/stock_sales_progress')
def stock_sales_progress():
    return jsonify({
        'stock_sales_progress': 65  # 固定为 65%
    })


# low_stock_alert
@app.route('/api/low_stock_alert')
def low_stock_alert():
    low_stock_products = product_data[product_data['Current Stock'] > 0].nsmallest(10, 'Current Stock')
    return jsonify({
        'products': low_stock_products['Product ID'].tolist(),
        'stocks': low_stock_products['Current Stock'].tolist()
    })

# abnormal_sales_stores
@app.route('/api/abnormal_sales_stores')
def abnormal_sales_stores():
    lowest_health_stores = store_data.nsmallest(10, 'Health Score')
    return jsonify({
        'stores': lowest_health_stores['Store ID'].tolist(),
        'health_scores': lowest_health_stores['Health Score'].round(2).tolist(),  # 保留2位小数
        'sales': lowest_health_stores['Sales (Last 3 Months)'].tolist()
    })


@app.route('/product-center')
def product_center():
    return render_template('product_center.html')

@app.route('/api/product-structure')
def product_structure():
    # 模拟商品结构分布的数据
    data = {
        'categories': ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5'],
        'sales': [300, 150, 200, 100, 250]  # 各类目对应的销量
    }
    return jsonify(data)
@app.route('/api/category-trends')
def category_trends():
    # 模拟分类目的近30天成交走势数据
    data = {
        'dates': ['2023-09-01', '2023-09-02', '2023-09-03', '2023-09-04', '2023-09-05'],
        'trends': [
            {'category': 'Category 1', 'sales': [50, 60, 70, 80, 90]},
            {'category': 'Category 2', 'sales': [30, 40, 50, 60, 70]},
            {'category': 'Category 3', 'sales': [20, 30, 40, 50, 60]},
            {'category': 'Category 4', 'sales': [10, 20, 30, 40, 50]},
        ]
    }
    return jsonify(data)
@app.route('/api/product-table')
def product_table():
    # 模拟商品聚合表的数据
    data = [
        {'name': 'Product 1', 'category': 'Category 1', 'brand': 'Brand A', 'stock': 100, 'sales30': 50, 'sales90': 150, 'isHot': True},
        {'name': 'Product 2', 'category': 'Category 2', 'brand': 'Brand B', 'stock': 200, 'sales30': 30, 'sales90': 90, 'isHot': False},
        {'name': 'Product 3', 'category': 'Category 3', 'brand': 'Brand C', 'stock': 150, 'sales30': 60, 'sales90': 180, 'isHot': True},
        {'name': 'Product 4', 'category': 'Category 4', 'brand': 'Brand D', 'stock': 80, 'sales30': 20, 'sales90': 70, 'isHot': False}
    ]
    return jsonify(data)


@app.route('/provincial-channel-center')
def provincial_channel_center():
    return render_template('provincial_channel_center.html')

# 省域成交占比堆积图数据 API
@app.route('/api/provincial-transaction-share')
def provincial_transaction_share():
    data = {
        'years': ['2023', '2024'],
        'provinces': ['Province 1', 'Province 2', 'Province 3', 'Province 4'],
        'transactions': {
            '2023': [0.3, 0.25, 0.2, 0.25],  # 2023年各省份的占比
            '2024': [0.4, 0.2, 0.3, 0.1]   # 2024年各省份的占比
        }
    }
    return jsonify(data)


# Top 3 和 Bottom 3 省份的成交趋势图数据 API
@app.route('/api/top-bottom-provinces-trends')
def top_bottom_provinces_trends():
    data = {
        'dates': ['2023-09-01', '2023-09-02', '2023-09-03', '2023-09-04'],
        'top_provinces': [
            {'province': 'Top 1', 'sales': [100, 120, 130, 150]},
            {'province': 'Top 2', 'sales': [90, 100, 110, 120]},
            {'province': 'Top 3', 'sales': [80, 90, 100, 110]}
        ],
        'bottom_provinces': [
            {'province': 'Bottom 1', 'sales': [10, 15, 20, 25]},
            {'province': 'Bottom 2', 'sales': [8, 10, 12, 15]},
            {'province': 'Bottom 3', 'sales': [5, 7, 10, 12]}
        ]
    }
    return jsonify(data)

# 省域成交表格明细 API
@app.route('/api/provincial-transaction-table')
def provincial_transaction_table():
    data = [
        {'province': 'Province 1', 'stores': 50, 'quantity': 1000, 'amount': 50000, 'brands': 10, 'avg_price': 50},
        {'province': 'Province 2', 'stores': 40, 'quantity': 800, 'amount': 40000, 'brands': 8, 'avg_price': 50},
        {'province': 'Province 3', 'stores': 30, 'quantity': 600, 'amount': 30000, 'brands': 6, 'avg_price': 50},
        {'province': 'Province 4', 'stores': 20, 'quantity': 400, 'amount': 20000, 'brands': 5, 'avg_price': 50}
    ]
    return jsonify(data)




@app.route('/store-management')
def store_management():
    return render_template('store_management.html')
# 门店分层占比数据 API
@app.route('/api/store-tier-distribution')
def store_tier_distribution():
    data = {
        'tiers': ['A', 'B', 'C', 'D', 'E', 'F'],
        'percentages': [0.1, 0.15, 0.2, 0.25, 0.2, 0.1]  # 各层级的占比
    }
    return jsonify(data)

# 各城市门店健康评分数据 API
@app.route('/api/city-health-scores')
def city_health_scores():
    data = {
        'cities': ['City 1', 'City 2', 'City 3', 'City 4'],
        'health_scores': [85, 90, 75, 80]  # 各城市门店的平均健康分
    }
    return jsonify(data)

# 门店清单表格 API
@app.route('/api/store-table')
def store_table():
    data = [
        {'store_id': 'S001', 'transaction_amount': 50000, 'health_score': 85, 'tier': 'A', 'province': 'Province 1', 'city': 'City 1', 'owner_id': 'O001', 'loan_status': True},
        {'store_id': 'S002', 'transaction_amount': 40000, 'health_score': 90, 'tier': 'B', 'province': 'Province 2', 'city': 'City 2', 'owner_id': 'O002', 'loan_status': False},
        {'store_id': 'S003', 'transaction_amount': 30000, 'health_score': 75, 'tier': 'C', 'province': 'Province 3', 'city': 'City 3', 'owner_id': 'O003', 'loan_status': True},
        {'store_id': 'S004', 'transaction_amount': 20000, 'health_score': 80, 'tier': 'D', 'province': 'Province 4', 'city': 'City 4', 'owner_id': 'O004', 'loan_status': False}
    ]
    return jsonify(data)




@app.route('/promotion-management')
def promotion_management():
    return render_template('promotion_management.html')

# 按省的销量数据 API (Top 8)
@app.route('/api/top-provinces-sales')
def top_provinces_sales():
    data = {
        'provinces': ['Province 1', 'Province 2', 'Province 3', 'Province 4', 'Province 5', 'Province 6', 'Province 7', 'Province 8'],
        'sales': [50000, 45000, 40000, 35000, 30000, 25000, 20000, 15000]
    }
    return jsonify(data)

# 分类目成交进度数据 API
@app.route('/api/category-transaction-progress')
def category_transaction_progress():
    data = {
        'categories': ['Category 1', 'Category 2', 'Category 3', 'Category 4'],
        'progress': [0.75, 0.6, 0.85, 0.7]  # 进度百分比
    }
    return jsonify(data)

# # # 复用省域成交表格 API (与 Provincial Channel Center 相同)
# @app.route('/api/provincial-transaction-table')
# def provincial_transaction_table():
#     data = [
#         {'province': 'Province 1', 'stores': 50, 'quantity': 1000, 'amount': 50000, 'brands': 10, 'avg_price': 50},
#         {'province': 'Province 2', 'stores': 40, 'quantity': 800, 'amount': 40000, 'brands': 8, 'avg_price': 50},
#         {'province': 'Province 3', 'stores': 30, 'quantity': 600, 'amount': 30000, 'brands': 6, 'avg_price': 50},
#         {'province': 'Province 4', 'stores': 20, 'quantity': 400, 'amount': 20000, 'brands': 5, 'avg_price': 50}
#     ]
#     return jsonify(data)




@app.route('/loan-center')
def loan_center():
    return render_template('loan_center.html')

@app.route('/accounting-center')
def accounting_center():
    return render_template('accounting_center.html')

@app.route('/supply-chain-management')
def supply_chain_management():
    return render_template('supply_chain_management.html')

@app.route('/data-permission-management')
def data_permission_management():
    return render_template('data_permission_management.html')

# @app.before_request
# def check_permissions():
#     # 检查用户是否有权限访问
#     if not user_is_authenticated():
#         return "You don't have access", 403
# 有无贷款门店的成交占比数据 API
@app.route('/api/loan-sales-distribution')
def loan_sales_distribution():
    data = {
        'categories': ['With Loan', 'Without Loan'],
        'sales': [60000, 40000]  # 有贷款和无贷款的门店成交额
    }
    return jsonify(data)

# 贷款还款率数据 API
@app.route('/api/loan-repayment-rate')
def loan_repayment_rate():
    data = {
        'categories': ['Repaid', 'Not Repaid'],
        'percentages': [0.8, 0.2]  # 已还款与未还款的比例
    }
    return jsonify(data)

# 门店贷款清单表格 API
@app.route('/api/loan-store-table')
def loan_store_table():
    data = [
        {'store_id': 'S001', 'city': 'City 1', 'province': 'Province 1', 'transaction_amount': 50000, 'loan_status': True, 'repayment_status': True},
        {'store_id': 'S002', 'city': 'City 2', 'province': 'Province 2', 'transaction_amount': 40000, 'loan_status': False, 'repayment_status': False},
        {'store_id': 'S003', 'city': 'City 3', 'province': 'Province 3', 'transaction_amount': 30000, 'loan_status': True, 'repayment_status': False},
        {'store_id': 'S004', 'city': 'City 4', 'province': 'Province 4', 'transaction_amount': 20000, 'loan_status': True, 'repayment_status': True}
    ]
    return jsonify(data)
# 门店明细表 API
@app.route('/api/store-details')
def store_details():
    data = [
        {'store_id': 'S001', 'transaction_amount': 50000, 'purchase_cost': 20000, 'sales_revenue': 60000, 'promotion_cost': 5000, 'logistics_cost': 2000, 'inventory_depreciation': 1000, 'ebita': 30000, 'ebita_rate': 0.5},
        {'store_id': 'S002', 'transaction_amount': 40000, 'purchase_cost': 15000, 'sales_revenue': 50000, 'promotion_cost': 4000, 'logistics_cost': 1800, 'inventory_depreciation': 800, 'ebita': 25000, 'ebita_rate': 0.45}
    ]
    return jsonify(data)

# 省域明细表 API
@app.route('/api/provincial-details')
def provincial_details():
    data = [
        {'province': 'Province 1', 'transaction_amount': 120000, 'purchase_cost': 60000, 'sales_revenue': 150000, 'promotion_cost': 10000, 'logistics_cost': 8000, 'inventory_depreciation': 5000, 'ebita': 70000, 'ebita_rate': 0.46},
        {'province': 'Province 2', 'transaction_amount': 100000, 'purchase_cost': 50000, 'sales_revenue': 130000, 'promotion_cost': 9000, 'logistics_cost': 7000, 'inventory_depreciation': 4000, 'ebita': 60000, 'ebita_rate': 0.45}
    ]
    return jsonify(data)

# 类目明细表 API
@app.route('/api/category-details')
def category_details():
    data = [
        {'category': 'Category 1', 'transaction_amount': 80000, 'purchase_cost': 30000, 'sales_revenue': 90000, 'promotion_cost': 7000, 'logistics_cost': 5000, 'inventory_depreciation': 3000, 'ebita': 40000, 'ebita_rate': 0.44},
        {'category': 'Category 2', 'transaction_amount': 70000, 'purchase_cost': 25000, 'sales_revenue': 85000, 'promotion_cost': 6000, 'logistics_cost': 4500, 'inventory_depreciation': 2500, 'ebita': 35000, 'ebita_rate': 0.41}
    ]
    return jsonify(data)


# 类目明细表 API
@app.route('/api/supply-category-details')
def supply_category_details():
    data = [
        {'product_id': 'P001', 'stock_remaining': 120, 'avg_storage_price': 45.5, '30_day_sales': 30, 'brand': 'Brand A'},
        {'product_id': 'P002', 'stock_remaining': 60, 'avg_storage_price': 30.0, '30_day_sales': 50, 'brand': 'Brand B'},
        {'product_id': 'P003', 'stock_remaining': 200, 'avg_storage_price': 55.0, '30_day_sales': 40, 'brand': 'Brand C'},
        {'product_id': 'P004', 'stock_remaining': 100, 'avg_storage_price': 25.0, '30_day_sales': 20, 'brand': 'Brand D'}
    ]
    return jsonify(data)

# 省份配送进度 API/api/provincial-delivery-progress
@app.route('/api/provincial-delivery-progress')
def provincial_delivery_progress():
    data = [
        {'province': 'Province 1', 'progress': 75},
        {'province': 'Province 2', 'progress': 60},
        {'province': 'Province 3', 'progress': 85},
        {'province': 'Province 4', 'progress': 90},
        {'province': 'Province 5', 'progress': 50}
    ]
    return jsonify(data)

# 权限申请记录 API (25 条数据)
@app.route('/api/permission-requests')
def permission_requests():
    data = [
        {'initiator': 'User A', 'role': 'Administrator', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-09-01 10:00', 'approval_time': '2024-09-02 14:00'},
        {'initiator': 'User B', 'role': 'Product Center', 'permission': 'View', 'approval': 'Denied', 'initiation_time': '2024-09-03 11:30', 'approval_time': '2024-09-04 09:20'},
        {'initiator': 'User C', 'role': 'Channel Manager', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-09-05 09:45', 'approval_time': '2024-09-05 16:15'},
        {'initiator': 'User D', 'role': 'Store Owner', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-09-06 08:20', 'approval_time': '2024-09-06 13:00'},
        {'initiator': 'User E', 'role': 'Channel Salesperson', 'permission': 'View', 'approval': 'Denied', 'initiation_time': '2024-09-07 07:15', 'approval_time': '2024-09-07 10:30'},
        {'initiator': 'User F', 'role': 'Product Center', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-09-08 12:00', 'approval_time': '2024-09-09 10:00'},
        {'initiator': 'User G', 'role': 'Store Owner', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-09-10 14:10', 'approval_time': '2024-09-11 16:50'},
        {'initiator': 'User H', 'role': 'Administrator', 'permission': 'View', 'approval': 'Denied', 'initiation_time': '2024-09-11 09:00', 'approval_time': '2024-09-12 13:00'},
        {'initiator': 'User I', 'role': 'Channel Manager', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-09-12 15:30', 'approval_time': '2024-09-13 12:40'},
        {'initiator': 'User J', 'role': 'Channel Salesperson', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-09-14 11:20', 'approval_time': '2024-09-15 14:30'},
        {'initiator': 'User K', 'role': 'Product Center', 'permission': 'View', 'approval': 'Denied', 'initiation_time': '2024-09-15 10:00', 'approval_time': '2024-09-16 08:50'},
        {'initiator': 'User L', 'role': 'Store Owner', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-09-16 09:15', 'approval_time': '2024-09-17 11:00'},
        {'initiator': 'User M', 'role': 'Administrator', 'permission': 'View', 'approval': 'Denied', 'initiation_time': '2024-09-18 13:00', 'approval_time': '2024-09-19 15:00'},
        {'initiator': 'User N', 'role': 'Channel Manager', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-09-20 08:30', 'approval_time': '2024-09-20 14:00'},
        {'initiator': 'User O', 'role': 'Product Center', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-09-21 09:50', 'approval_time': '2024-09-22 12:00'},
        {'initiator': 'User P', 'role': 'Channel Salesperson', 'permission': 'Manage', 'approval': 'Denied', 'initiation_time': '2024-09-22 10:30', 'approval_time': '2024-09-23 13:00'},
        {'initiator': 'User Q', 'role': 'Administrator', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-09-23 12:20', 'approval_time': '2024-09-24 11:00'},
        {'initiator': 'User R', 'role': 'Store Owner', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-09-25 13:40', 'approval_time': '2024-09-26 14:20'},
        {'initiator': 'User S', 'role': 'Product Center', 'permission': 'Manage', 'approval': 'Denied', 'initiation_time': '2024-09-26 09:15', 'approval_time': '2024-09-27 10:40'},
        {'initiator': 'User T', 'role': 'Channel Manager', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-09-27 11:00', 'approval_time': '2024-09-28 14:30'},
        {'initiator': 'User U', 'role': 'Administrator', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-09-29 10:20', 'approval_time': '2024-09-30 16:00'},
        {'initiator': 'User V', 'role': 'Channel Salesperson', 'permission': 'View', 'approval': 'Denied', 'initiation_time': '2024-09-30 09:30', 'approval_time': '2024-10-01 12:20'},
        {'initiator': 'User W', 'role': 'Store Owner', 'permission': 'Manage', 'approval': 'Approved', 'initiation_time': '2024-10-01 14:00', 'approval_time': '2024-10-02 10:00'},
        {'initiator': 'User X', 'role': 'Channel Manager', 'permission': 'Manage', 'approval': 'Denied', 'initiation_time': '2024-10-02 11:30', 'approval_time': '2024-10-03 09:10'},
        {'initiator': 'User Y', 'role': 'Administrator', 'permission': 'View', 'approval': 'Approved', 'initiation_time': '2024-10-03 08:50', 'approval_time': '2024-10-04 11:20'}
    ]
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

