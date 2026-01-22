import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Messages from "../components/Messages";
import "../styles/pages/catalog.css";

function MainPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [services, setServices] = useState([]);
  const [filteredServices, setFilteredServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState([]);
  const [cartCount, setCartCount] = useState(0);

  // Данные точно как в Django шаблоне
  const demoServices = [
    {
      id: 1,
      title: "Главный учебный корпус МГТУ",
      description: "г. Москва, 2-я Бауманская ул., д. 5, стр. 1",
      category: "Учебный корпус",
      icon: "fa-university",
      area: "25000",
      rooms: "200",
      floor: "5",
      total_floors: "5",
      price: "150 000 000",
      image_url: "/static/images/building1.jpg",
      full_description:
        "Главный корпус МГТУ им. Н.Э. Баумана - историческое здание, в котором расположены основные факультеты и администрация университета.",
    },
    {
      id: 2,
      title: "Учебно-лабораторный корпус МГТУ",
      description: "г. Москва, Рубцовская наб., д. 2/18",
      category: "Лабораторный корпус",
      icon: "fa-flask",
      area: "18000",
      rooms: "150",
      floor: "7",
      total_floors: "7",
      price: "120 000 000",
      image_url: "/static/images/building2.jpg",
      full_description:
        "Учебно-лабораторный корпус МГТУ им. Н.Э. Баумана оснащен современным оборудованием для проведения научных исследований.",
    },
    {
      id: 3,
      title: "Спортивный комплекс МГТУ",
      description: "г. Москва, Госпитальная наб., д. 4/2",
      category: "Спорткомплекс",
      icon: "fa-dumbbell",
      area: "12000",
      rooms: "50",
      floor: "3",
      total_floors: "3",
      price: "80 000 000",
      image_url: "/static/images/building3.png",
      full_description:
        "Спортивный комплекс МГТУ им. Н.Э. Баумана включает в себя бассейн, тренажерные залы, залы для игровых видов спорта.",
    },
  ];

  useEffect(() => {
    // Имитация загрузки
    setTimeout(() => {
      setServices(demoServices);
      setFilteredServices(demoServices);
      setLoading(false);

      // Получаем количество в корзине
      const cart = JSON.parse(localStorage.getItem("cart") || "[]");
      setCartCount(cart.length);
    }, 500);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const filtered = services.filter(
        (service) =>
          service.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          service.description
            .toLowerCase()
            .includes(searchQuery.toLowerCase()) ||
          service.category.toLowerCase().includes(searchQuery.toLowerCase()),
      );
      setFilteredServices(filtered);
    } else {
      setFilteredServices(services);
    }
  };

  const handleAddToCart = (serviceId) => {
    const service = services.find((s) => s.id === serviceId);
    if (!service) return;

    // Получаем текущую корзину
    const cart = JSON.parse(localStorage.getItem("cart") || "[]");

    // Проверяем, есть ли уже этот объект в корзине
    const existingItem = cart.find((item) => item.id === serviceId);

    if (existingItem) {
      // Увеличиваем количество
      existingItem.quantity += 1;
    } else {
      // Добавляем новый объект
      cart.push({
        id: serviceId,
        title: service.title,
        description: service.description,
        category: service.category,
        area: service.area,
        total_floors: service.total_floors,
        price: service.price,
        image_url: service.image_url,
        quantity: 1,
      });
    }

    // Сохраняем в localStorage
    localStorage.setItem("cart", JSON.stringify(cart));
    setCartCount(cart.length);

    // Показываем сообщение как в Django
    setMessages([
      {
        type: "success",
        text: `Объект "${service.title}" добавлен в заявку`,
      },
    ]);

    // Автоматически скрываем сообщение через 3 секунды
    setTimeout(() => {
      setMessages([]);
    }, 3000);
  };

  return (
    <div className="catalog-page">
      <Messages messages={messages} />

      {/* Секция поиска */}
      <section className="search-section">
        <div className="container">
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              placeholder="Поиск по строительным объектам..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-link">
              Найти
            </button>
          </form>

          {/* Результаты поиска */}
          {searchQuery && (
            <div className="search-results">
              {filteredServices.length > 0 ? (
                <p>
                  Найдено результатов: {filteredServices.length} по запросу "
                  {searchQuery}"
                </p>
              ) : (
                <p>
                  По запросу "{searchQuery}" ничего не найдено. Попробуйте
                  изменить запрос.
                </p>
              )}
            </div>
          )}
        </div>
      </section>

      {/* Каталог объектов */}
      <main>
        <div className="container">
          {loading ? (
            <div className="no-services">
              <h3>Загрузка объектов...</h3>
            </div>
          ) : filteredServices.length === 0 ? (
            <div className="no-services">
              <h3>Объекты не найдены</h3>
              <p>Попробуйте изменить поисковый запрос</p>
            </div>
          ) : (
            <div className="properties-grid">
              {filteredServices.map((service) => (
                <div key={service.id} className="property-card">
                  <div className="property-image">
                    <img src={service.image_url} alt={service.title} />
                  </div>
                  <div className="property-content">
                    <div className="property-type">{service.category}</div>
                    <h3>{service.title}</h3>
                    <p className="address">{service.description}</p>
                    <div className="specs">
                      <span>{service.area} м²</span>
                      <span>{service.total_floors} этаж(ей)</span>
                    </div>
                    <div className="price">{service.price} ₽</div>
                    <div className="property-actions">
                      <Link
                        to={`/service/${service.id}`}
                        className="hero-back-link"
                      >
                        Подробнее
                      </Link>
                      <button
                        onClick={() => handleAddToCart(service.id)}
                        className="hero-back-link"
                      >
                        <i className="fas fa-cart-plus"></i> В заявку
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default MainPage;
