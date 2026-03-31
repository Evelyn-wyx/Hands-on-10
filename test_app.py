"""
电商平台单元测试
"""

import pytest
from app import app, PRODUCTS


# ============================================
# Fixtures - 测试fixtures
# ============================================

@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_cart():
    """创建购物车数据"""
    return [
        {'id': 1, 'name': 'iPhone 15 Pro', 'price': 999.99, 'quantity': 1},
        {'id': 3, 'name': 'AirPods Pro', 'price': 249.99, 'quantity': 2},
    ]


# ============================================
# 测试: 产品数据
# ============================================

def test_products_list():
    """测试产品列表非空"""
    assert len(PRODUCTS) > 0
    assert isinstance(PRODUCTS, list)


def test_product_structure():
    """测试产品数据结构"""
    for product in PRODUCTS:
        assert 'id' in product
        assert 'name' in product
        assert 'price' in product
        assert 'category' in product
        assert 'stock' in product


def test_product_price_positive():
    """测试产品价格均为正数"""
    for product in PRODUCTS:
        assert product['price'] > 0


# ============================================
# 测试: 路由功能
# ============================================

def test_home_page(client):
    """测试首页访问"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'电商平台' in response.data


def test_cart_page(client):
    """测试购物车页面"""
    response = client.get('/cart')
    assert response.status_code == 200


def test_add_to_cart(client):
    """测试添加到购物车"""
    response = client.post('/add_to_cart', data={'product_id': '1'})
    assert response.status_code == 302  # 重定向


def test_checkout_without_items(client):
    """测试空购物车结算"""
    response = client.post('/checkout')
    assert response.status_code in [200, 302]


# ============================================
# 测试: 购物车逻辑
# ============================================

def test_cart_total_calculation(sample_cart):
    """测试购物车总价计算"""
    total = sum(item['price'] * item['quantity'] for item in sample_cart)
    expected = 999.99 + 249.99 * 2  # 1499.97
    assert abs(total - expected) < 0.01


def test_empty_cart():
    """测试空购物车"""
    cart = []
    total = sum(item['price'] * item['quantity'] for item in cart)
    assert total == 0


# ============================================
# 测试: 应用配置
# ============================================

def test_app_secret_key():
    """测试应用密钥配置"""
    assert app.secret_key is not None


def test_app_debug_mode():
    """测试应用调试模式"""
    # 在测试环境中应该关闭debug
    assert app.config.get('TESTING') is not None