"""
数据清理和合并脚本
用于处理电商平台的客户和订单数据
"""

import sqlite3
import os
from datetime import datetime

def init_database():
    """初始化数据库连接"""
    db_path = 'ecommerce.db'
    conn = sqlite3.connect(db_path)
    return conn, db_path

def create_tables(conn):
    """创建数据表"""
    cursor = conn.cursor()
    
    # 创建客户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            total_amount REAL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    
    conn.commit()
    print("✅ 数据表创建成功")

def clean_customer_data(data):
    """清理客户数据"""
    cleaned = []
    for record in data:
        # 去除空白字符
        name = record.get('name', '').strip()
        email = record.get('email', '').strip().lower()
        phone = record.get('phone', '').strip()
        address = record.get('address', '').strip()
        
        # 验证邮箱格式
        if '@' not in email:
            print(f"⚠️ 跳过无效邮箱: {email}")
            continue
        
        cleaned.append({
            'name': name,
            'email': email,
            'phone': phone,
            'address': address
        })
    
    return cleaned

def merge_customer_data(conn, customers):
    """合并客户数据到数据库"""
    cursor = conn.cursor()
    merged_count = 0
    
    for customer in customers:
        try:
            cursor.execute('''
                INSERT INTO customers (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            ''', (customer['name'], customer['email'], 
                  customer.get('phone', ''), customer.get('address', '')))
            merged_count += 1
        except sqlite3.IntegrityError:
            # 邮箱已存在，跳过
            print(f"⚠️ 客户 {customer['name']} 已存在，跳过")
            continue
    
    conn.commit()
    print(f"✅ 成功合并 {merged_count} 条客户记录")

def process_orders(conn, orders):
    """处理订单数据"""
    cursor = conn.cursor()
    processed_count = 0
    
    for order in orders:
        try:
            total = order.get('quantity', 1) * order.get('price', 0)
            cursor.execute('''
                INSERT INTO orders (customer_id, product_name, quantity, price, total_amount, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order.get('customer_id'), order.get('product_name', ''),
                  order.get('quantity', 1), order.get('price', 0), 
                  total, order.get('status', 'pending')))
            processed_count += 1
        except Exception as e:
            print(f"⚠️ 订单处理失败: {e}")
            continue
    
    conn.commit()
    print(f"✅ 成功处理 {processed_count} 条订单记录")

def generate_report(conn):
    """生成数据报告"""
    cursor = conn.cursor()
    
    # 客户统计
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    
    # 订单统计
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    
    # 销售额统计
    cursor.execute("SELECT SUM(total_amount) FROM orders")
    total_revenue = cursor.fetchone()[0] or 0
    
    # 订单状态统计
    cursor.execute("SELECT status, COUNT(*) FROM orders GROUP BY status")
    status_counts = cursor.fetchall()
    
    print("\n" + "="*50)
    print("📊 数据报告")
    print("="*50)
    print(f"总客户数: {customer_count}")
    print(f"总订单数: {order_count}")
    print(f"总销售额: ¥{total_revenue:.2f}")
    print("\n订单状态分布:")
    for status, count in status_counts:
        print(f"  - {status}: {count}")
    print("="*50)

def main():
    """主函数 - 执行数据清理和合并流程"""
    print("🚀 开始数据清理和合并...")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 初始化数据库
    conn, db_path = init_database()
    print(f"📁 数据库: {db_path}")
    
    # 创建表
    create_tables(conn)
    
    # 模拟客户数据
    sample_customers = [
        {'name': '张三', 'email': 'zhangsan@example.com', 'phone': '13800138000', 'address': '北京'},
        {'name': '李四', 'email': 'lisi@example.com', 'phone': '13900139000', 'address': '上海'},
        {'name': '王五', 'email': 'wangwu@example.com', 'phone': '13700137000', 'address': '广州'},
    ]
    
    # 清理并合并客户数据
    cleaned_customers = clean_customer_data(sample_customers)
    merge_customer_data(conn, cleaned_customers)
    
    # 模拟订单数据
    sample_orders = [
        {'customer_id': 1, 'product_name': 'iPhone 15 Pro', 'quantity': 1, 'price': 999.99, 'status': 'completed'},
        {'customer_id': 1, 'product_name': 'AirPods Pro', 'quantity': 2, 'price': 249.99, 'status': 'completed'},
        {'customer_id': 2, 'product_name': 'MacBook Pro 16', 'quantity': 1, 'price': 2499.99, 'status': 'pending'},
        {'customer_id': 3, 'product_name': 'iPad Air', 'quantity': 1, 'price': 599.99, 'status': 'shipped'},
    ]
    
    # 处理订单
    process_orders(conn, sample_orders)
    
    # 生成报告
    generate_report(conn)
    
    conn.close()
    print("\n✅ 数据处理完成!")

if __name__ == '__main__':
    main()
