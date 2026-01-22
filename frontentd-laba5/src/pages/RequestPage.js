import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Messages from '../components/Messages';
import '../styles/pages/request.css';

function RequestPage() {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Загружаем корзину из localStorage
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    setCartItems(cart);
    setLoading(false);
  }, []);

  const handleDeleteRequest = () => {
    if (window.confirm('Вы уверены, что хотите удалить заявку?')) {
      // Очищаем корзину
      localStorage.removeItem('cart');
      setCartItems([]);
      
      // Показываем сообщение
      setMessages([{ 
        type: 'success', 
        text: 'Заявка успешно удалена' 
      }]);
      
      // Перенаправляем на главную через 1.5 секунды
      setTimeout(() => {
        navigate('/');
      }, 1500);
    }
  };

  const handleViewDetails = (requestId) => {
    navigate(`/build-request/${requestId}`);
  };

  const calculateTotalPrice = () => {
    return cartItems.reduce((total, item) => {
      // Убираем пробелы из цены и преобразуем в число
      const price = parseInt(item.price.replace(/\s/g, '')) || 0;
      return total + (price * item.quantity);
    }, 0).toLocaleString('ru-RU');
  };

  if (loading) {
    return (
      <div className="request-page">
        <div className="container">
          <div className="no-services">
            <h3>Загрузка заявки...</h3>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="request-page">
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
          {cartItems.length > 0 ? (
            <div className="request-container">
              <div className="request-header">
                <h1 className="request-title">Заявка на технический надзор</h1>
                <span className="request-status status-draft">Черновик</span>
              </div>

              <div className="table-responsive">
                <table className="request-table">
                  <thead>
                    <tr>
                      <th>Изображение</th>
                      <th>Объект</th>
                      <th>Местоположение</th>
                      <th>Площадь</th>
                      <th>Количество</th>
                      <th>Цена</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cartItems.map((item, index) => (
                      <tr key={index}>
                        <td style={{ width: '80px' }}>
                          <img
                            src={item.image_url}
                            alt={item.title}
                            className="product-thumbnail"
                          />
                        </td>
                        <td>
                          <Link to={`/service/${item.id}`}>
                            {item.title}
                          </Link>
                        </td>
                        <td>{item.description}</td>
                        <td>{item.area} м²</td>
                        <td>{item.quantity}</td>
                        <td>{item.price} ₽</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="request-summary">
                <div>
                  <span>Всего объектов: </span>
                  <strong>{cartItems.length}</strong>
                </div>
                <div className="total-price">
                  Итого: {calculateTotalPrice()} ₽
                </div>
              </div>

              <div className="request-actions">
                <button 
                  onClick={() => handleViewDetails(1)}
                  className="hero-back-link"
                >
                  Просмотреть детали заявки
                </button>
                
                <button 
                  onClick={handleDeleteRequest}
                  className="hero-back-link"
                  style={{ backgroundColor: '#dc3545' }}
                >
                  Удалить заявку
                </button>
              </div>
            </div>
          ) : (
            <div className="empty-request">
              <h3>В вашей заявке нет строительных объектов.</h3>
              <p>Добавьте объекты из каталога, чтобы создать заявку на технический надзор.</p>
              <Link to="/" className="hero-back-link">
                Перейти к выбору объектов
              </Link>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default RequestPage;