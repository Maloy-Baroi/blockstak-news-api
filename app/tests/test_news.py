import pytest
from fastapi.testclient import TestClient
from unittest import mock
from datetime import datetime
from httpx import Response

from app.main import app
from app.models.latest_news import News


def test_get_news(client, test_access_headers):
    # Mock the httpx.AsyncClient.get method
    with mock.patch("httpx.AsyncClient.get") as mock_get:
        # Define our mock response
        mock_response = Response(
            200,
            json={
                "status": "ok",
                "totalResults": 2,
                "articles": [
                    {
                        "source": {"id": "test-source", "name": "Test Source"},
                        "author": "Test Author",
                        "title": "Test Title 1",
                        "description": "Test Description 1",
                        "url": "https://example.com/1",
                        "urlToImage": "https://example.com/image1.jpg",
                        "publishedAt": "2023-05-01T12:00:00Z",
                        "content": "Test content 1"
                    },
                    {
                        "source": {"id": "test-source-2", "name": "Test Source 2"},
                        "author": "Test Author 2",
                        "title": "Test Title 2",
                        "description": "Test Description 2",
                        "url": "https://example.com/2",
                        "urlToImage": "https://example.com/image2.jpg",
                        "publishedAt": "2023-05-02T12:00:00Z",
                        "content": "Test content 2"
                    }
                ]
            }
        )
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get("/api/v1/news/news", headers=test_access_headers)
        
        # Assert that the response status code is 200 OK
        assert response.status_code == 200
        
        # Assert that the mock was called
        mock_get.assert_called_once()
        
        # Check the response data
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 2
        assert data["total"] == 2
        assert data["page"] == 1
        assert data["limit"] == 10

        # Check first article data
        assert data["data"][0]["title"] == "Test Title 1"
        assert data["data"][0]["description"] == "Test Description 1"
        assert data["data"][0]["url"] == "https://example.com/1"
        assert data["data"][0]["source"] == "Test Source"


def test_save_latest_news(client, db, test_access_headers):
    # Mock the httpx.AsyncClient.get method
    with mock.patch("httpx.AsyncClient.get") as mock_get:
        # Define our mock response
        mock_response = Response(
            200,
            json={
                "status": "ok",
                "totalResults": 3,
                "articles": [
                    {
                        "source": {"id": "test-source", "name": "Test Source"},
                        "author": "Test Author",
                        "title": "Test Title 1",
                        "description": "Test Description 1",
                        "url": "https://example.com/1",
                        "urlToImage": "https://example.com/image1.jpg",
                        "publishedAt": "2023-05-01T12:00:00Z",
                        "content": "Test content 1"
                    },
                    {
                        "source": {"id": "test-source-2", "name": "Test Source 2"},
                        "author": "Test Author 2",
                        "title": "Test Title 2",
                        "description": "Test Description 2",
                        "url": "https://example.com/2",
                        "urlToImage": "https://example.com/image2.jpg",
                        "publishedAt": "2023-05-02T12:00:00Z",
                        "content": "Test content 2"
                    },
                    {
                        "source": {"id": "test-source-3", "name": "Test Source 3"},
                        "author": "Test Author 3",
                        "title": "Test Title 3",
                        "description": "Test Description 3",
                        "url": "https://example.com/3",
                        "urlToImage": "https://example.com/image3.jpg",
                        "publishedAt": "2023-05-03T12:00:00Z",
                        "content": "Test content 3"
                    }
                ]
            }
        )
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.post("/api/v1/news/news/save-latest", headers=test_access_headers)
        
        # Assert that the response status code is 201 CREATED
        assert response.status_code == 201
        
        # Assert that the mock was called
        mock_get.assert_called_once()
        
        # Check the response data
        data = response.json()
        assert data["message"] == "Successfully saved top 3 latest news"
        assert data["saved_count"] == 3
        
        # Check that news was saved to the database
        news_items = db.query(News).all()
        assert len(news_items) == 3
        assert news_items[0].title == "Test Title 1"
        assert news_items[1].title == "Test Title 2"
        assert news_items[2].title == "Test Title 3"


def test_get_headlines_by_country(client, test_access_headers):
    # Mock the httpx.AsyncClient.get method
    with mock.patch("httpx.AsyncClient.get") as mock_get:
        # Define our mock response
        mock_response = Response(
            200,
            json={
                "status": "ok",
                "totalResults": 1,
                "articles": [
                    {
                        "source": {"id": "test-source", "name": "Test Source"},
                        "author": "Test Author",
                        "title": "Test Country Headline",
                        "description": "Test Description",
                        "url": "https://example.com/country",
                        "urlToImage": "https://example.com/country.jpg",
                        "publishedAt": "2023-05-01T12:00:00Z",
                        "content": "Test country content"
                    }
                ]
            }
        )
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get("/api/v1/news/news/headlines/country/us", headers=test_access_headers)
        
        # Assert that the response status code is 200 OK
        assert response.status_code == 200
        
        # Assert that the mock was called
        mock_get.assert_called_once()
        
        # Check the response data
        data = response.json()
        assert data["status"] == "ok"
        assert len(data["articles"]) == 1
        assert data["articles"][0]["title"] == "Test Country Headline"


def test_get_headlines_by_source(client, test_access_headers):
    # Mock the httpx.AsyncClient.get method
    with mock.patch("httpx.AsyncClient.get") as mock_get:
        # Define our mock response
        mock_response = Response(
            200,
            json={
                "status": "ok",
                "totalResults": 1,
                "articles": [
                    {
                        "source": {"id": "test-source", "name": "Test Source"},
                        "author": "Test Author",
                        "title": "Test Source Headline",
                        "description": "Test Description",
                        "url": "https://example.com/source",
                        "urlToImage": "https://example.com/source.jpg",
                        "publishedAt": "2023-05-01T12:00:00Z",
                        "content": "Test source content"
                    }
                ]
            }
        )
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get("/api/v1/news/news/headlines/source/bbc-news", headers=test_access_headers)
        
        # Assert that the response status code is 200 OK
        assert response.status_code == 200
        
        # Assert that the mock was called
        mock_get.assert_called_once()
        
        # Check the response data
        data = response.json()
        assert data["status"] == "ok"
        assert len(data["articles"]) == 1
        assert data["articles"][0]["title"] == "Test Source Headline"


def test_get_headlines_by_filter(client, test_access_headers):
    # Mock the httpx.AsyncClient.get method
    with mock.patch("httpx.AsyncClient.get") as mock_get:
        # Define our mock response
        mock_response = Response(
            200,
            json={
                "status": "ok",
                "totalResults": 1,
                "articles": [
                    {
                        "source": {"id": "test-source", "name": "Test Source"},
                        "author": "Test Author",
                        "title": "Test Filter Headline",
                        "description": "Test Description",
                        "url": "https://example.com/filter",
                        "urlToImage": "https://example.com/filter.jpg",
                        "publishedAt": "2023-05-01T12:00:00Z",
                        "content": "Test filter content"
                    }
                ]
            }
        )
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get(
            "/api/v1/news/news/headlines/filter?country=us&source=bbc-news", 
            headers=test_access_headers
        )
        
        # Assert that the response status code is 200 OK
        assert response.status_code == 200
        
        # Assert that the mock was called
        mock_get.assert_called_once()
        
        # Check the response data
        data = response.json()
        assert data["status"] == "ok"
        assert len(data["articles"]) == 1
        assert data["articles"][0]["title"] == "Test Filter Headline"