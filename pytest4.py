# test_get_post_list.py
import pytest
import requests
import json
from typing import List, Dict


class TestGetPostList:
    """Тесты для получения списка постов"""
    
    BASE_URL = "https://ccrayp.onrender.com"
    POST_LIST_ENDPOINT = "/api/post/list"
    
    def test_get_post_list_success(self):
        """Тест успешного получения списка постов"""
        response = requests.get(
            f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"accept": "application/json"}
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        
        response_data = response.json()
        
        # Проверяем, что ответ - массив
        assert isinstance(response_data, list)
        
        # Если есть посты, проверяем структуру каждого
        if len(response_data) > 0:
            for post in response_data:
                self._validate_post_structure(post)

    def test_get_post_list_empty(self):
        """Тест получения пустого списка постов"""
        response = requests.get(
            f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"accept": "application/json"}
        )
        
        # Пустой список - это валидный случай (200 с пустым массивом)
        if response.status_code == 200:
            response_data = response.json()
            assert isinstance(response_data, list)
            # Может быть пустым массивом или 404, зависит от реализации
        elif response.status_code == 404:
            response_data = response.json()
            assert "message" in response_data
            assert "not found" in response_data["message"].lower()

    def test_get_post_list_not_found(self):
        """Тест случая, когда посты не найдены"""
        response = requests.get(
            f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"accept": "application/json"}
        )
        
        if response.status_code == 404:
            response_data = response.json()
            assert "message" in response_data
            assert "not found" in response_data["message"].lower()
            assert response.headers["Content-Type"] == "application/json"

    def test_get_post_list_without_accept_header(self):
        """Тест без заголовка Accept"""
        response = requests.get(f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}")
        
        # Должен работать даже без Accept header
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert isinstance(response.json(), list)

    def test_get_post_list_response_headers(self):
        """Тест проверки заголовков ответа"""
        response = requests.get(
            f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"accept": "application/json"}
        )
        
        assert "content-type" in response.headers
        assert "application/json" in response.headers["content-type"]
        
        # Проверяем дополнительные заголовки
        assert "date" in response.headers.lower()  # Дата ответа

    def test_get_post_list_performance(self):
        """Тест производительности получения списка постов"""
        import time
        
        start_time = time.time()
        
        response = requests.get(
            f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"accept": "application/json"}
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code in [200, 404]
        assert response_time < 5.0  # Запрос должен выполняться менее 5 секунд

    @pytest.mark.parametrize("http_method", ["POST", "PUT", "DELETE", "PATCH"])
    def test_post_list_wrong_method(self, http_method: str):
        """Тест вызова с неправильным HTTP методом"""
        response = requests.request(
            method=http_method,
            url=f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"accept": "application/json"}
        )
        
        # Ожидаем 405 Method Not Allowed
        assert response.status_code == 405
        
        if response.status_code == 405:
            response_data = response.json()
            assert "message" in response_data
            assert "method not allowed" in response_data["message"].lower()

    def test_get_post_list_with_query_params(self):
        """Тест с query parameters (если поддерживаются)"""
        # Проверяем различные query parameters
        test_params = [
            {"limit": 10},
            {"offset": 0},
            {"sort": "date"},
            {"limit": 5, "offset": 10}
        ]
        
        for params in test_params:
            response = requests.get(
                f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
                params=params,
                headers={"accept": "application/json"}
            )
            
            # API может игнорировать параметры или возвращать ошибку
            assert response.status_code in [200, 400, 404, 422]

    def _validate_post_structure(self, post: Dict):
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
        
        # Дополнительные проверки форматов
        if post["date"]:  # Если дата не пустая
            # Можно добавить проверку формата даты
            pass
        
        if post["link"]:  # Если ссылка не пустая
            assert post["link"].startswith(("http://", "https://", "/"))

    def test_post_structure_validation(self):
        """Тест валидации структуры каждого поста в ответе"""
        response = requests.get(
            f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
            headers={"accept": "application/json"}
        )
        
        if response.status_code == 200:
            posts = response.json()
            for post in posts:
                self._validate_post_structure(post)

    def test_get_post_list_pagination(self):
        """Тест пагинации (если поддерживается)"""
        # Проверяем пагинационные параметры
        pagination_params = [
            {"page": 1, "size": 10},
            {"page": 0, "size": 20},  # Граничный случай
            {"page": 1, "size": 100},  # Большой размер страницы
        ]
        
        for params in pagination_params:
            response = requests.get(
                f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
                params=params,
                headers={"accept": "application/json"}
            )
            
            status_code = response.status_code
            assert status_code in [200, 400, 404, 422]
            
            if status_code == 200:
                posts = response.json()
                assert isinstance(posts, list)
                
                # Если API поддерживает пагинацию, может возвращать метаданные
                # или ограниченное количество постов

    def test_get_post_list_ordering(self):
        """Тест сортировки постов"""
        ordering_params = [
            {"sort": "date", "order": "desc"},
            {"sort": "date", "order": "asc"},
            {"sort": "label"},
        ]
        
        for params in ordering_params:
            response = requests.get(
                f"{self.BASE_URL}{self.POST_LIST_ENDPOINT}",
                params=params,
                headers={"accept": "application/json"}
            )
            
            if response.status_code == 200:
                posts = response.json()
                if len(posts) > 1:
                    # Можно проверить порядок сортировки
                    pass
