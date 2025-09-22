# test_create_post.py
import pytest
import requests
import json
from typing import Dict, Any


class TestCreatePost:
    """Тесты для создания нового поста"""
    
    BASE_URL = "https://ccrayp.onnder.com"
    CREATE_POST_ENDPOINT = "/api/post/new"
    LOGIN_ENDPOINT = "/api/login"
    
    @pytest.fixture
    def valid_token(self) -> str:
        """Получение валидного JWT токена"""
        credentials = {"username": "test_user", "password": "test_password"}
        
        response = requests.post(
            f"{self.BASE_URL}{self.LOGIN_ENDPOINT}",
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            pytest.skip("Cannot get valid token - authentication failed")
    
    @pytest.fixture
    def valid_post_data(self) -> Dict[str, Any]:
        """Валидные данные для создания поста"""
        return {
            "date": "2024-01-15",
            "img": "/images/test.jpg",
            "label": "Test Post",
            "link": "/test-post",
            "mode": True,
            "text": "This is a test post content"
        }
    
    @pytest.fixture
    def auth_headers(self, valid_token: str) -> Dict[str, str]:
        """Заголовки аутентификации"""
        return {
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    def test_create_post_success(self, auth_headers: Dict, valid_post_data: Dict):
        """Тест успешного создания поста"""
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=valid_post_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        
        response_data = response.json()
        
        # Проверяем структуру успешного ответа
        assert "message" in response_data
        assert "successfully" in response_data["message"].lower()

    def test_create_post_unauthorized(self, valid_post_data: Dict):
        """Тест создания поста без авторизации"""
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=valid_post_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 401

    def test_create_post_invalid_token(self, valid_post_data: Dict):
        """Тест создания поста с невалидным токеном"""
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=valid_post_data,
            headers={
                "Authorization": "Bearer invalid_token_123",
                "Content-Type": "application/json"
            }
        )
        
        assert response.status_code == 401

    @pytest.mark.parametrize("missing_field", [
        "date", "img", "label", "link", "mode", "text"
    ])
    def test_create_post_missing_required_fields(self, auth_headers: Dict, valid_post_data: Dict, missing_field: str):
        """Тест отсутствия обязательных полей"""
        post_data = valid_post_data.copy()
        del post_data[missing_field]
        
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=post_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        response_data = response.json()
        assert "message" in response_data
        assert "missing" in response_data["message"].lower()
        assert missing_field in response_data["message"]

    def test_create_post_empty_fields(self, auth_headers: Dict):
        """Тест с пустыми полями"""
        empty_post_data = {
            "date": "",
            "img": "",
            "label": "",  # Обязательное поле не должно быть пустым
            "link": "",
            "mode": True,
            "text": ""
        }
        
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=empty_post_data,
            headers=auth_headers
        )
        
        # Ожидаем 400 за пустые обязательные поля
        assert response.status_code in [400, 422]

    @pytest.mark.parametrize("invalid_mode", [
        "true",  # Строка вместо boolean
        "false",
        "1",
        "0",
        "yes",
        "no"
    ])
    def test_create_post_invalid_mode_type(self, auth_headers: Dict, valid_post_data: Dict, invalid_mode: str):
        """Тест с невалидным типом для поля mode"""
        post_data = valid_post_data.copy()
        post_data["mode"] = invalid_mode
        
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=post_data,
            headers=auth_headers
        )
        
        # Ожидаем 400 за невалидный тип данных
        assert response.status_code in [400, 422]

    def test_create_post_with_extra_fields(self, auth_headers: Dict, valid_post_data: Dict):
        """Тест с дополнительными полями"""
        post_data = valid_post_data.copy()
        post_data["extra_field"] = "extra value"
        post_data["another_field"] = 123
        
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=post_data,
            headers=auth_headers
        )
        
        # Дополнительные поля должны игнорироваться или вызывать ошибку
        assert response.status_code in [200, 400]

    def test_create_post_invalid_json(self, auth_headers: Dict):
        """Тест с невалидным JSON"""
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            data="invalid json data",
            headers=auth_headers
        )
        
        assert response.status_code in [400, 415]

    def test_create_post_wrong_content_type(self, auth_headers: Dict, valid_post_data: Dict):
        """Тест с неправильным Content-Type"""
        headers = auth_headers.copy()
        headers["Content-Type"] = "text/plain"
        
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=valid_post_data,
            headers=headers
        )
        
        assert response.status_code in [400, 415, 200]  # Зависит от реализации

    @pytest.mark.parametrize("http_method", ["GET", "PUT", "DELETE", "PATCH"])
    def test_create_post_wrong_method(self, auth_headers: Dict, valid_post_data: Dict, http_method: str):
        """Тест с неправильным HTTP методом"""
        response = requests.request(
            method=http_method,
            url=f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=valid_post_data,
            headers=auth_headers
        )
        
        assert response.status_code == 405
        response_data = response.json()
        assert "message" in response_data
        assert "method not allowed" in response_data["message"].lower()

    def test_create_post_duplicate(self, auth_headers: Dict, valid_post_data: Dict):
        """Тест создания дубликата поста"""
        # Первое создание
        response1 = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=valid_post_data,
            headers=auth_headers
        )
        
        if response1.status_code == 200:
            # Второе создание с теми же данными
            response2 = requests.post(
                f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
                json=valid_post_data,
                headers=auth_headers
            )
            
            # Может вернуть 200, 400 или 409 в зависимости от логики дубликатов
            assert response2.status_code in [200, 400, 409]

    @pytest.mark.parametrize("field,value", [
        ("label", "A" * 1000),  # Очень длинный label
        ("text", "A" * 10000),  # Очень длинный текст
        ("link", "A" * 1000),   # Очень длинная ссылка
        ("img", "A" * 1000),    # Очень длинный URL изображения
    ])
    def test_create_post_field_length_limits(self, auth_headers: Dict, valid_post_data: Dict, field: str, value: str):
        """Тест ограничений длины полей"""
        post_data = valid_post_data.copy()
        post_data[field] = value
        
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=post_data,
            headers=auth_headers
        )
        
        # Может вернуть 200 или 400 в зависимости от валидации
        assert response.status_code in [200, 400]

    def test_create_post_special_characters(self, auth_headers: Dict):
        """Тест со специальными символами"""
        special_post_data = {
            "date": "2024-01-15",
            "img": "/images/test.jpg",
            "label": "Test & Post <with> \"special' characters",
            "link": "/test-post?param=value&another=param",
            "mode": True,
            "text": "Text with \n newlines \t tabs and \\ backslashes"
        }
        
        response = requests.post(
            f"{self.BASE_URL}{self.CREATE_POST_ENDPOINT}",
            json=special_post_data,
            headers=auth_headers
        )
        
        assert response.status_code in [200, 400]
