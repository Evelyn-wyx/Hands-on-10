"""
电商平台主应用
包含产品展示、购物车、订单处理等功能
"""

from flask import Flask, render_template_string, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'ecommerce-secret-key-2024'

# 产品数据
PRODUCTS = [
    {"id": 1, "name": "iPhone 15 Pro", "price": 999.99, "category": "电子产品", "stock": 50},
    {"id": 2, "name": "MacBook Pro 16", "price": 2499.99, "category": "电子产品", "stock": 30},
    {"id": 3, "name": "AirPods Pro", "price": 249.99, "category": "音频设备", "stock": 100},
    {"id": 4, "name": "iPad Air", "price": 599.99, "category": "平板电脑", "stock": 45},
    {"id": 5, "name": "Apple Watch", "price": 399.99, "category": "智能穿戴", "stock": 60},
    {"id": 6, "name": "Sony PS5", "price": 499.99, "category": "游戏设备", "stock": 25},
]

# HTML模板
HOME_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>电商平台 - 首页</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header h1 { display: inline-block; }
        .nav { float: right; margin-top: 5px; }
        .nav a { color: white; text-decoration: none; margin-left: 20px; padding: 8px 16px; border-radius: 20px; transition: background 0.3s; }
        .nav a:hover { background: rgba(255,255,255,0.2); }
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }
        .products { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .product-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.3s, box-shadow 0.3s; }
        .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .product-name { font-size: 18px; font-weight: 600; margin-bottom: 10px; color: #333; }
        .product-category { color: #888; font-size: 14px; margin-bottom: 10px; }
        .product-price { font-size: 24px; color: #e74c3c; font-weight: bold; margin-bottom: 15px; }
        .product-stock { color: #27ae60; font-size: 14px; margin-bottom: 15px; }
        .btn { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 25px; transition: background 0.3s; border: none; cursor: pointer; }
        .btn:hover { background: #5568d3; }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .cart-badge { background: #e74c3c; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-left: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛒 电商平台</h1>
        <div class="nav">
            <a href="/">首页</a>
            <a href="/cart">购物车 <span class="cart-badge">{{ cart_count }}</span></a>
        </div>
    </div>
    <div class="container">
        <h2 style="margin-bottom: 20px;">热门产品</h2>
        <div class="products">
            {% for product in products %}
            <div class="product-card">
                <div class="product-name">{{ product.name }}</div>
                <div class="product-category">{{ product.category }}</div>
                <div class="product-price">¥{{ "%.2f"|format(product.price) }}</div>
                <div class="product-stock">库存: {{ product.stock }}</div>
                <form method="POST" action="/add_to_cart">
                    <input type="hidden" name="product_id" value="{{ product.id }}">
                    <button type="submit" class="btn" {% if product.stock == 0 %}disabled{% endif %}>
                        {% if product.stock == 0 %}缺货{% else %}加入购物车{% endif %}
                    </button>
                </form>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

CART_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>购物车 - 电商平台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
        .header h1 { display: inline-block; }
        .nav { float: right; }
        .nav a { color: white; text-decoration: none; margin-left: 20px; }
        .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        .cart-item { background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .cart-item-info h3 { margin-bottom: 5px; }
        .cart-item-price { color: #e74c3c; font-size: 20px; font-weight: bold; }
        .total { background: white; border-radius: 12px; padding: 20px; text-align: right; font-size: 24px; font-weight: bold; }
        .btn { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 25px; border: none; cursor: pointer; }
        .btn-danger { background: #e74c3c; }
        .empty { text-align: center; padding: 50px; color: #888; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛒 购物车</h1>
        <div class="nav">
            <a href="/">返回首页</a>
        </div>
    </div>
    <div class="container">
        {% if cart_items %}
            {% for item in cart_items %}
            <div class="cart-item">
                <div class="cart-item-info">
                    <h3>{{ item.name }}</h3>
                    <p>单价: ¥{{ "%.2f"|format(item.price) }}</p>
                </div>
                <div>
                    <span class="cart-item-price">¥{{ "%.2f"|format(item.price * item.quantity) }}</span>
                    <form method="POST" action="/remove_from_cart" style="display:inline; margin-left: 15px;">
                        <input type="hidden" name="product_id" value="{{ item.id }}">
                        <button type="submit" class="btn btn-danger">删除</button>
                    </form>
                </div>
            </div>
            {% endfor %}
            <div class="total">
                总计: ¥{{ "%.2f"|format(total) }}
                <form method="POST" action="/checkout" style="display:inline; margin-left: 20px;">
                    <button type="submit" class="btn">结算</button>
                </form>
            </div>
        {% else %}
            <div class="empty">
                <h2>购物车是空的</h2>
                <p><a href="/">去购物</a></p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """首页 - 展示产品列表"""
    cart = session.get('cart', [])
    cart_count = len(cart)
    return render_template_string(HOME_HTML, products=PRODUCTS, cart_count=cart_count)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """将产品添加到购物车"""
    product_id = int(request.form.get('product_id', 0))
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    
    if product and product['stock'] > 0:
        cart = session.get('cart', [])
        # 检查是否已存在
        existing_item = next((item for item in cart if item['id'] == product_id), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            })
        session['cart'] = cart
    
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    """购物车页面"""
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template_string(CART_HTML, cart_items=cart_items, total=total)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    """从购物车移除产品"""
    product_id = int(request.form.get('product_id', 0))
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    """结账处理"""
    cart = session.get('cart', [])
    if cart:
        # 这里可以添加订单处理逻辑
        session['cart'] = []
        return """
        <!DOCTYPE html>
        <html>
        <head><title>订单成功</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>✅ 订单提交成功！</h1>
            <p>感谢您的购买</p>
            <a href="/" style="color: #667eea;">返回首页</a>
        </body>
        </html>
        """
    return redirect(url_for('home'))

if __name__ == '__main__':
    # 启动Flask应用
    print("🛒 电商平台启动中...")
    print("访问 http://127.0.0.1:5000 查看")
    app.run(debug=True, host='0.0.0.0', port=5000)
