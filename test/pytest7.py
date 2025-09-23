# test_get_post_by_id.py
import pytest
import requests
import json
from typing import Dict, Any


class TestGetPostById:
    """Тесты для получения поста по ID"""
    
    BASE_URL = "https://ccrayp.onrender.com"
    GET_POST_BY_ID_ENDPOINT = "/api/post/{id}"
    LOGIN_ENDPOINT = "/api/login"
    POST_LIST_ENDPOINT = "/api/post/list"
    
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
    def existing_post_id(self, valid_token: str) -> int:
        """Получение ID существующего поста"""
        response = requests.get(
            f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        
        if response.status_code == 200 and len(response.json()) > 0:
            # Предполагаем, что посты имеют поле 'id'
            return response.json()[0].get('id', 1)  # Fallback to 1 if no id field
        else:
            pytest.skip("No existing posts found for testing")
    
    @pytest.fixture
    def non_existing_post_id(self) -> int:
        """ID несуществующего поста"""
        return 999999
    
    @pytest.fixture
    def auth_headers(self, valid_token: str) -> Dict[str, str]:
        """Заголовки аутентификации"""
        return {
            "Authorization": f"Bearer {valid_token}",
            "accept": "application/json"
        }

    def test_get_post_success(self, auth_headers: Dict, existing_post_id: int):
        """Тест успешного получения поста по ID"""
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        
        response_data = response.json()
        
        # Проверяем структуру поста
        self._validate_post_structure(response_data)

    def test_get_post_not_found(self, auth_headers: Dict, non_existing_post_id: int):
        """Тест получения несуществующего поста"""
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=non_existing_post_id)}",
            headers=auth_headers
        )
        
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data
        assert "does not exist" in response_data["message"].lower()

    def test_get_post_unauthorized(self, existing_post_id: int):
        """Тест получения поста без авторизации"""
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers={"accept": "application/json"}
        )
        
        assert response.status_code == 401

    def test_get_post_invalid_token(self, existing_post_id: int):
        """Тест получения поста с невалидным токеном"""
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers={
                "Authorization": "Bearer invalid_token_123",
                "accept": "application/json"
            }
        )
        
        assert response.status_code == 401

    @pytest.mark.parametrize("invalid_id", [
        "invalid",    # Строка вместо числа
        "1.5",        # Float вместо integer
        "0",          # Нулевой ID
        "-1",         # Отрицательный ID
        "9999999999999999999999999999",  # Очень большое число
        "",           # Пустая строка
        "null",       # null как строка
        "undefined",  # undefined как строка
    ])
    def test_get_post_invalid_id_format(self, auth_headers: Dict, invalid_id: str):
        """Тест с невалидными форматами ID"""
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=invalid_id)}",
            headers=auth_headers
        )
        
        # Ожидаем 400 за невалидный ID
        assert response.status_code == 400
        if response.status_code == 400:
            response_data = response.json()
            assert "message" in response_data
            assert "invalid id" in response_data["message"].lower()

    def test_get_post_without_accept_header(self, auth_headers: Dict, existing_post_id: int):
        """Тест без заголовка Accept"""
        headers = auth_headers.copy()
        del headers["accept"]
        
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers=headers
        )
        
        # Должен работать даже без Accept header
        assert response.status_code in [200, 401]

    def test_get_post_response_headers(self, auth_headers: Dict, existing_post_id: int):
        """Тест проверки заголовков ответа"""
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers=auth_headers
        )
        
        if response.status_code == 200:
            assert "content-type" in response.headers
            assert "application/json" in response.headers["content-type"]
            assert "date" in response.headers.lower()

    def test_get_post_performance(self, auth_headers: Dict, existing_post_id: int):
        """Тест производительности получения поста"""
        import time
        
        start_time = time.time()
        
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers=auth_headers
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code in [200, 404]
        assert response_time < 3.0  # Запрос должен выполняться менее 3 секунд

    @pytest.mark.parametrize("http_method", ["POST", "PUT", "DELETE", "PATCH"])
    def test_get_post_wrong_method(self, auth_headers: Dict, existing_post_id: int, http_method: str):
        """Тест с неправильным HTTP методом"""
        response = requests.request(
            method=http_method,
            url=f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers=auth_headers
        )
        
        assert response.status_code == 405
        response_data = response.json()
        assert "message" in response_data
        assert "method not allowed" in response_data["message"].lower()

    def test_get_post_consistency(self, auth_headers: Dict, existing_post_id: int):
        """Тест консистентности данных при многократных запросах"""
        responses_data = []
        
        # Делаем несколько запросов подряд
        for i in range(3):
            response = requests.get(
                f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
                headers=auth_headers
            )
            
            if response.status_code == 200:
                responses_data.append(response.json())
        
        # Проверяем консистентность ответов
        if len(responses_data) > 1:
            for i in range(1, len(responses_data)):
                assert responses_data[i] == responses_data[0]

    def _validate_post_structure(self, post: Dict[str, Any]):
        """Валидация структуры объекта поста"""
        required_fields = ["date", "img", "label", "link", "mode", "text"]
        
        for field in required_fields:
            assert field in post, f"Missing required field: {field}"
        
        # Проверяем типы данных
        assert isinstance(post["date"], str)
        assert isinstance(post["img"], str)
        assert isinstance(post["label"], str)
        assert isinstance(post["link"], str)
        assert isinstance(post["mode"], bool)
        assert isinstance(post["text"], str)
        
        # Дополнительные проверки
        assert post["label"] != "", "Label should not be empty"
        assert post["text"] != "", "Text should not be empty"

    def test_post_structure_validation(self, auth_headers: Dict, existing_post_id: int):
        """Тест валидации структуры поста"""
        response = requests.get(
            f"{self.BASE_URL}{self.GET_POST_BY_ID_ENDPOINT.format(id=existing_post_id)}",
            headers=auth_headers
        )
        
        if response.status_code == 200:
            post = response.json()
            self._validate_post_structure(post)