# Пример из коллекции Postman (postman_collection.json)
{
	"info": {
		"_postman_id": "a5b3c7d9-e1f2-4g5h-6i7j-8k9l0m1n2o3p",
		"name": "Construction Services API",
		"description": "API для управления строительными услугами и заявками",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
	},
	"item": [
		{
			"name": "Услуги (BuildingObject)",
			"item": [
				{
					"name": "Получить список услуг",
					"request": {
						"method": "GET",
						"url": {
							"raw": "http://localhost:8000/api/services/",
							"protocol": "http",
							"host": ["localhost"],
							"port": "8000",
							"path": ["api", "services", ""]
						},
						"description": "Получение списка всех услуг"
					}
				},
				{
					"name": "Получить список услуг с фильтрацией",
					"request": {
						"method": "GET",
						"url": {
							"raw": "http://localhost:8000/api/services/?area=100&floor_count=2",
							"protocol": "http",
							"host": ["localhost"],
							"port": "8000",
							"path": ["api", "services", ""],
							"query": [
								{
									"key": "area",
									"value": "100"
								},
								{
									"key": "floor_count",
									"value": "2"
								}
							]
						},
						"description": "Получение списка услуг с фильтрацией по площади и количеству этажей"
					}
				}
			]
		},
		{
			"name": "Заявки (ConstructionRequest)",
			"item": [
				{
					"name": "Получить иконку корзины",
					"request": {
						"method": "GET",
						"url": {
							"raw": "http://localhost:8000/api/cart-icon/",
							"protocol": "http",
							"host": ["localhost"],
							"port": "8000",
							"path": ["api", "cart-icon", ""]
						},
						"description": "Получение информации о корзине (заявке-черновике) текущего пользователя"
					}
				}
			]
		}
	]
}