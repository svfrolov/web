import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Messages from '../components/Messages';
import '../styles/pages/catalog.css';

function MainPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [services, setServices] = useState([]);
  const [filteredServices, setFilteredServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState([]);
  const [cartCount, setCartCount] = useState(0);

  // === ДЕМО-ДАННЫЕ С ИСПРАВЛЕННЫМИ ПУТЯМИ ===
  const demoServices = [
    {
      id: 1,
      title: 'Главный учебный корпус МГТУ',
      description: 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
      category: 'Учебный корпус',
      icon: 'fa-university',
      area: '25000',
      rooms: '200',
      floor: '5',
      total_floors: '5',
      price: '150 000 000',
      // Вариант 1: Django static
      image_url: 'http://127.0.0.1:8000/static/images/building1.jpg',
      // Вариант 2: Если скопировали в React
      // image_url: '/images/building1.jpg',
      full_description: 'Главный корпус МГТУ им. Н.Э. Баумана.',
      location: 'Москва, 2-я Бауманская ул., 5, стр. 1',
      features: ['Историческое здание', 'Аудитории с проекторами']
    },
    {
      id: 2,
      title: 'Учебно-лабораторный корпус МГТУ',
      description: 'г. Москва, Рубцовская наб., д. 2/18',
      category: 'Лабораторный корпус',
      icon: 'fa-flask',
      area: '18000',
      rooms: '150',
      floor: '7',
      total_floors: '7',
      price: '120 000 000',
      image_url: 'http://127.0.0.1:8000/static/images/building2.jpg',
      full_description: 'Современный учебно-лабораторный комплекс.',
      location: 'Москва, Рубцовская наб., 2/18',
      features: ['Чистые комнаты', 'Испытательные стенды']
    },
    {
      id: 3,
      title: 'Спортивный комплекс МГТУ',
      description: 'г. Москва, Госпитальная наб., д. 4/2',
      category: 'Спорткомплекс',
      icon: 'fa-dumbbell',
      area: '12000',
      rooms: '50',
      floor: '3',
      total_floors: '3',
      price: '80 000 000',
      // ВАЖНО: building3.png, а не .jpg!
      image_url: 'http://127.0.0.1:8000/static/images/building3.png',
      full_description: 'Многофункциональный спортивный комплекс.',
      location: 'Москва, Госпитальная наб., 4/2',
      features: ['Бассейн 25м', 'Тренажерные залы']
    }
  ];

  // Функция для безопасной загрузки изображений
  const handleImageError = (e, service) => {
    console.log(`Ошибка загрузки: ${service.image_url}`);
    // Используем placeholder как fallback
    const colors = {
      'Учебный корпус': '3498db',
      'Лабораторный корпус': '2ecc71',
      'Спорткомплекс': 'e74c3c',
    };
    const color = colors[service.category] || '95a5a6';
    e.target.src = `https://via.placeholder.com/400x300/${color}/ffffff?text=${encodeURIComponent(service.category)}`;
  };

  useEffect(() => {
    setTimeout(() => {
      setServices(demoServices);
      setFilteredServices(demoServices);
      setLoading(false);
      
      const cart = JSON.parse(localStorage.getItem('cart') || '[]');
      setCartCount(cart.length);
    }, 500);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const filtered = demoServices.filter(service =>
        service.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        service.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredServices(filtered);
    } else {
      setFilteredServices(demoServices);
    }
  };

  const handleAddToCart = (serviceId) => {
    const service = demoServices.find(s => s.id === serviceId);
    if (!service) return;

    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const existingItem = cart.find(item => item.id === serviceId);
    
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cart.push({
        id: serviceId,
        title: service.title,
        description: service.description,
        category: service.category,
        area: service.area,
        total_floors: service.total_floors,
        price: service.price,
        image_url: service.image_url,
        quantity: 1
      });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    setCartCount(cart.length);
    
    setMessages([{ 
      type: 'success', 
      text: `"${service.title}" добавлен в заявку` 
    }]);
    
    setTimeout(() => setMessages([]), 3000);
  };

  return (
    <div className="catalog-page">
      <Messages messages={messages} />
      
      <section>
        <div className="container">
          <h1 className="page-title">Каталог объектов МГТУ</h1>
        </div>
      </section>

      <section className="search-section">
        <div className="container">
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              placeholder="Поиск объектов..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-link">
              Найти
            </button>
          </form>
        </div>
      </section>

      <main>
        <div className="container">
          {loading ? (
            <div className="no-services">
              <h3>Загрузка...</h3>
            </div>
          ) : filteredServices.length === 0 ? (
            <div className="no-services">
              <h3>Объекты не найдены</h3>
              <p>Попробуйте изменить запрос</p>
            </div>
          ) : (
            <div className="properties-grid">
              {filteredServices.map(service => (
                <div key={service.id} className="property-card">
                  <div className="property-image">
                    <img 
                      src={service.image_url}
                      alt={service.title}
                      onError={(e) => handleImageError(e, service)}
                    />
                  </div>
                  <div className="property-content">
                    <div className="property-type">
                      <i className={`fas ${service.icon}`}></i> {service.category}
                    </div>
                    <h3>{service.title}</h3>
                    <p className="address">{service.description}</p>
                    <div className="specs">
                      <span>{service.area} м²</span>
                      <span>{service.total_floors} эт.</span>
                    </div>
                    <div className="price">{service.price} ₽</div>
                    <div className="property-actions">
                      <Link to={`/service/${service.id}`} className="hero-back-link">
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