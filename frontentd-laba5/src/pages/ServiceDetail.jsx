import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import Messages from '../components/Messages';
import '../styles/pages/detail.css';

function ServiceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState([]);

  // Данные точно как в Django шаблоне
  const servicesData = {
    1: {
      title: 'Главный корпус МГТУ',
      description: 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
      category: 'Учебный корпус',
      icon: 'fa-university',
      area: '25000',
      rooms: '200',
      floor: '5',
      total_floors: '5',
      price: '150 000 000',
      full_description: 'Главный корпус МГТУ им. Н.Э. Баумана - историческое здание, в котором расположены основные факультеты и администрация университета. Здесь проходят занятия студентов большинства технических специальностей.',
      location: 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
      image_url: '/static/images/building1.jpg'
    },
    2: {
      title: 'Учебно-лабораторный корпус МГТУ',
      description: 'г. Москва, Рубцовская наб., д. 2/18',
      category: 'Лабораторный корпус',
      icon: 'fa-flask',
      area: '18000',
      rooms: '150',
      floor: '7',
      total_floors: '7',
      price: '120 000 000',
      full_description: 'Учебно-лабораторный корпус МГТУ им. Н.Э. Баумана оснащен современным оборудованием для проведения научных исследований и лабораторных работ. Здесь расположены специализированные лаборатории и научные центры.',
      location: 'г. Москва, Рубцовская наб., д. 2/18',
      image_url: '/static/images/building2.jpg'
    },
    3: {
      title: 'Спортивный комплекс МГТУ',
      description: 'г. Москва, Госпитальная наб., д. 4/2',
      category: 'Спорткомплекс',
      icon: 'fa-dumbbell',
      area: '12000',
      rooms: '50',
      floor: '3',
      total_floors: '3',
      price: '80 000 000',
      full_description: 'Спортивный комплекс МГТУ им. Н.Э. Баумана включает в себя бассейн, тренажерные залы, залы для игровых видов спорта и легкой атлетики. Здесь проводятся занятия по физической культуре и тренировки спортивных команд университета.',
      location: 'г. Москва, Госпитальная наб., д. 4/2',
      image_url: '/static/images/building3.png'
    }
  };

  useEffect(() => {
    setTimeout(() => {
      const serviceId = parseInt(id);
      const selectedService = servicesData[serviceId] || servicesData[1];
      setService(selectedService);
      setLoading(false);
    }, 500);
  }, [id]);

  const handleAddToCart = () => {
    if (!service) return;

    // Получаем текущую корзину
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    
    // Проверяем, есть ли уже этот объект в корзине
    const existingItem = cart.find(item => item.id === parseInt(id));
    
    if (existingItem) {
      // Увеличиваем количество
      existingItem.quantity += 1;
    } else {
      // Добавляем новый объект
      cart.push({
        id: parseInt(id),
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
    
    // Сохраняем в localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Показываем сообщение как в Django
    setMessages([{ 
      type: 'success', 
      text: `Объект "${service.title}" добавлен в заявку` 
    }]);
    
    // Автоматически скрываем сообщение через 3 секунды
    setTimeout(() => {
      setMessages([]);
    }, 3000);
  };

  if (loading) {
    return (
      <div className="detail-page">
        <div className="container">
          <div className="no-services">
            <h3>Загрузка информации об объекте...</h3>
          </div>
        </div>
      </div>
    );
  }

  if (!service) {
    return (
      <div className="detail-page">
        <div className="container">
          <div className="no-services">
            <h3>Объект не найден</h3>
            <p>Запрошенный объект не существует</p>
            <Link to="/" className="hero-back-link">Вернуться в каталог</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="detail-page">
      <Messages messages={messages} />
      
      <section>
        <div className="container">
          <p>
            <Link to="/" className="hero-back-link">
              Назад к объектам
            </Link>
          </p>
        </div>
      </section>

      <main>
        <div className="container">
          <div className="detail-page-card">
            {/* Изображение объекта */}
            <div className="detail-page-image">
              <img src={service.image_url} alt={service.title} />
            </div>

            <div className="detail-page-content">
              <div className="property-type">{service.category}</div>
              <h1 className="detail-page-title">{service.title}</h1>
              <p className="address">{service.description}</p>

              {/* Характеристики */}
              <div className="detail-page-specs">
                <div className="spec-item">
                  <span className="spec-icon">📐</span>
                  <div>
                    <div className="spec-label">Площадь</div>
                    <div className="spec-value">{service.area} м²</div>
                  </div>
                </div>
                <div className="spec-item">
                  <span className="spec-icon">🏢</span>
                  <div>
                    <div className="spec-label">Этажей</div>
                    <div className="spec-value">{service.total_floors}</div>
                  </div>
                </div>
                <div className="spec-item">
                  <span className="spec-icon">🏛️</span>
                  <div>
                    <div className="spec-label">Тип</div>
                    <div className="spec-value">{service.category}</div>
                  </div>
                </div>
              </div>

              <div className="detail-page-price">{service.price} ₽</div>

              {/* Кнопки действий */}
              <div className="action-buttons">
                <button onClick={handleAddToCart} className="btn btn-primary">
                  <i className="fas fa-cart-plus"></i> Добавить в заявку
                </button>
                <Link to="/request" className="btn btn-outline-primary">
                  <i className="fas fa-shopping-cart"></i> Перейти к заявке
                </Link>
              </div>

              {/* Описание */}
              <div className="info-box">
                <div className="info-box-header">Описание</div>
                <div className="info-box-body">
                  <p>{service.full_description}</p>
                </div>
              </div>

              {/* Расположение */}
              <div className="info-box">
                <div className="info-box-header">Расположение</div>
                <div className="info-box-body">
                  <p>📍 {service.location}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ServiceDetail;