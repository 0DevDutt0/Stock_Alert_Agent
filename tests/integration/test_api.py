"""Integration tests for API endpoints"""

import pytest


@pytest.mark.integration
def test_root_endpoint(test_client):
    """Test root endpoint"""
    response = test_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.integration
def test_health_endpoint(test_client):
    """Test health check endpoint"""
    response = test_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "dependencies" in data


@pytest.mark.integration
def test_analyze_stock_endpoint(test_client):
    """Test stock analysis endpoint"""
    payload = {
        "symbol": "AAPL",
        "buy_price": 150.0,
        "target_price": 180.0
    }
    
    response = test_client.post("/api/v1/stocks/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "current_price" in data
    assert "decision" in data


@pytest.mark.integration
def test_track_stock_endpoint(test_client):
    """Test track stock endpoint"""
    payload = {
        "symbol": "AAPL",
        "buy_price": 150.0,
        "target_price": 180.0
    }
    
    response = test_client.post("/api/v1/stocks/track", json=payload)
    
    # May fail if stock already tracked, but should return 200 or 409
    assert response.status_code in [200, 409]


@pytest.mark.integration
def test_list_stocks_endpoint(test_client):
    """Test list stocks endpoint"""
    response = test_client.get("/api/v1/stocks")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.integration
def test_run_agent_endpoint(test_client):
    """Test agent run endpoint"""
    response = test_client.get("/api/v1/agent/run")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_stocks" in data
    assert "results" in data
    assert "time_ist" in data
