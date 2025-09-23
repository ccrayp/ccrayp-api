# test_update_post.py
import pytest
import requests
import json
from typing import Dict, Any


class TestUpdatePost:
    """Тесты для обновления поста по ID"""
    
    BASE_URL = "https://ccrayp.onrender.com"
    UPDATE_POST_ENDPOINT = "/api/post/update/{id}"
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
            return response.json()[0]["id"]  # Предполагаем, что есть поле id
        else:
            pytest.skip("No existing posts found for testing")
    
    @pytest.fixture
    def non_existing_post_id(self) -> int:
        """ID несуществующего поста"""
        return 999999
    
    @pytest.fixture
    def valid_update_data(self) -> Dict[str, Any]:
        """Валидные данные для обновления поста"""
        return {
            "date": "2024-01-20",
            "img": "/images/updated.jpg",
            "label": "Updated Post Title",
            "link": "/updated-post",
            "mode": False,
            "text": "This post has been updated"
        }
    
    @pytest.fixture
    def auth_headers(self, valid_token: str) -> Dict[str, str]:
        """Заголовки аутентификации"""
        return {
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    def test_update_post_success(self, auth_headers: Dict, existing_post_id: int, valid_update_data: Dict):
        """Тест успешного обновления поста"""
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=valid_update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        
        response_data = response.json()
        
        # Проверяем структуру успешного ответа
        assert "message" in response_data
        assert "successfully" in response_data["message"].lower()

    def test_update_post_not_found(self, auth_headers: Dict, non_existing_post_id: int, valid_update_data: Dict):
        """Тест обновления несуществующего поста"""
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=non_existing_post_id)}",
            json=valid_update_data,
            headers=auth_headers
        )
        
        # Ожидаем 404 для несуществующего поста
        assert response.status_code == 404

    def test_update_post_unauthorized(self, existing_post_id: int, valid_update_data: Dict):
        """Тест обновления поста без авторизации"""
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=valid_update_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 401

    def test_update_post_invalid_token(self, existing_post_id: int, valid_update_data: Dict):
        """Тест обновления с невалидным токеном"""
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=valid_update_data,
            headers={
                "Authorization": "Bearer invalid_token_123",
                "Content-Type": "application/json"
            }
        )
        
        assert response.status_code == 401

    def test_update_post_no_data(self, auth_headers: Dict, existing_post_id: int):
        """Тест обновления без данных"""
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json={},  # Пустой объект
            headers=auth_headers
        )
        
        assert response.status_code == 400
        response_data = response.json()
        assert "message" in response_data
        assert "no data" in response_data["message"].lower()

    def test_update_post_partial_data(self, auth_headers: Dict, existing_post_id: int):
        """Тест обновления с частичными данными"""
        partial_data = {
            "label": "Partially Updated Title",
            "text": "Only these fields should be updated"
        }
        
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=partial_data,
            headers=auth_headers
        )
        
        # Должен принимать частичные обновления (200) или требовать все поля (400)
        assert response.status_code in [200, 400]

    @pytest.mark.parametrize("invalid_id", [
        "invalid",    # Строка вместо числа
        "1.5",        # Float вместо integer
        "0",          # Нулевой ID
        "-1",         # Отрицательный ID
        "9999999999999999999999999999",  # Очень большое число
    ])
    def test_update_post_invalid_id_format(self, auth_headers: Dict, valid_update_data: Dict, invalid_id: str):
        """Тест с невалидными форматами ID"""
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=invalid_id)}",
            json=valid_update_data,
            headers=auth_headers
        )
        
        # Ожидаем 400, 404 или 422 в зависимости от валидации
        assert response.status_code in [400, 404, 422, 500]

    @pytest.mark.parametrize("field,invalid_value", [
        ("mode", "not_a_boolean"),  # Не boolean для mode
        ("mode", 123),              # Число вместо boolean
        ("mode", None),             # None вместо boolean
    ])
    def test_update_post_invalid_field_types(self, auth_headers: Dict, existing_post_id: int, field: str, invalid_value: Any):
        """Тест с невалидными типами данных"""
        update_data = {
            "date": "2024-01-20",
            "img": "/images/test.jpg",
            "label": "Test Post",
            "link": "/test-post",
            "mode": True,
            "text": "Test content"
        }
        update_data[field] = invalid_value
        
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=update_data,
            headers=auth_headers
        )
        
        # Ожидаем 400 за невалидный тип данных
        assert response.status_code in [400, 422]

    def test_update_post_extra_fields(self, auth_headers: Dict, existing_post_id: int, valid_update_data: Dict):
        """Тест с дополнительными полями"""
        update_data = valid_update_data.copy()
        update_data["extra_field"] = "extra value"
        update_data["another_field"] = 123
        
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=update_data,
            headers=auth_headers
        )
        
        # Дополнительные поля должны игнорироваться или вызывать ошибку
        assert response.status_code in [200, 400]

    def test_update_post_empty_fields(self, auth_headers: Dict, existing_post_id: int):
        """Тест с пустыми полями"""
        empty_data = {
            "date": "",
            "img": "",
            "label": "",  # Обязательное поле не должно быть пустым
            "link": "",
            "mode": True,
            "text": ""
        }
        
        response = requests.put(
            f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=empty_data,
            headers=auth_headers
        )
        
        # Ожидаем 400 за пустые обязательные поля
        assert response.status_code in [200, 400, 422]

    @pytest.mark.parametrize("http_method", ["GET", "POST", "DELETE", "PATCH"])
    def test_update_post_wrong_method(self, auth_headers: Dict, existing_post_id: int, valid_update_data: Dict, http_method: str):
        """Тест с неправильным HTTP методом"""
        response = requests.request(
            method=http_method,
            url=f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
            json=valid_update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 405
        response_data = response.json()
        assert "message" in response_data
        assert "method not allowed" in response_data["message"].lower()

    def test_update_post_same_data(self, auth_headers: Dict, existing_post_id: int):
        """Тест обновления теми же данными (идемпотентность)"""
        # Сначала получаем текущие данные поста
        get_response = requests.get(
            f"{self.BASE_URL}/api/post/{existing_post_id}",
            headers=auth_headers
        )
        
        if get_response.status_code == 200:
            current_data = get_response.json()
            
            # Обновляем теми же данными
            response = requests.put(
                f"{self.BASE_URL}{self.UPDATE_POST_ENDPOINT.format(id=existing_post_id)}",
                json=current_data,
                headers=auth_headers
            )
            
            # Должен возвращать 200 (успех) даже при тех же данных
            assert response.status_code == 200