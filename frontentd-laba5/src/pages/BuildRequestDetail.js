import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import Messages from '../components/Messages';
import '../styles/pages/request.css';

function BuildRequestDetail() {
  const { orderId } = useParams();
  const [buildRequest, setBuildRequest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState([]);

  // Данные для демонстрации (как в Django)
  const demoBuildRequests = {
    1: {
      id: 1,
      user_name: 'Иванов Иван Иванович',
      email: 'ivanov@example.com',
      phone: '+7 (999) 123-45-67',
      payment_method: 'Банковская карта',
      operation_type: 'Технический надзор',
      status: 'submitted',
      created_date: '15.10.2023',
      get_status_display: 'Сформирован',
      is_deleted: false,
      items: [
        {
          product: {
            title: 'Главный учебный корпус МГТУ',
            description: 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
            category: 'Учебный корпус',
            icon: 'fa-university',
            area: '25000',
            rooms: '200',
            floor: '5',
            total_floors: '5',
            price: '150000000',
            image_url: '/static/images/building1.jpg'
          },
          quantity: 1,
          order_number: 1
        },
        {
          product: {
            title: 'Учебно-лабораторный корпус МГТУ',
            description: 'г. Москва, Рубцовская наб., д. 2/18',
            category: 'Лабораторный корпус',
            icon: 'fa-flask',
            area: '18000',
            rooms: '150',
            floor: '7',
            total_floors: '7',
            price: '120000000',
            image_url: '/static/images/building2.jpg'
          },
          quantity: 1,
          order_number: 2
        }
      ],
      total_price: '270000000',
      service: {
        title: 'Главный учебный корпус МГТУ',
        image_url: '/static/images/building1.jpg'
      }
    }
  };

  useEffect(() => {
    setTimeout(() => {
      const requestId = parseInt(orderId);
      const selectedRequest = demoBuildRequests[requestId] || demoBuildRequests[1];
      
      if (selectedRequest.is_deleted) {
        setMessages([{
          type: 'warning',
          text: `Заявка #${orderId} была удалена и отображается только для просмотра.`
        }]);
      }
      
      setBuildRequest(selectedRequest);
      setLoading(false);
    }, 500);
  }, [orderId]);

  const getStatusClass = (status) => {
    switch(status) {
      case 'deleted': return 'status-deleted';
      case 'draft': return 'status-draft';
      case 'submitted': return 'status-submitted';
      case 'completed': return 'status-completed';
      case 'rejected': return 'status-rejected';
      case 'not_found': return 'status-not-found';
      default: return 'status-draft';
    }
  };

  if (loading) {
    return (
      <div className="detail-page">
        <div className="container">
          <div className="no-services">
            <h3>Загрузка информации о заявке...</h3>
          </div>
        </div>
      </div>
    );
  }

  if (!buildRequest) {
    return (
      <div className="detail-page">
        <div className="container">
          <div className="no-services">
            <h3>Заявка не найдена</h3>
            <p>Запрошенная заявка не существует</p>
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
              Назад к корпусам
            </Link>
          </p>
        </div>
      </section>

      <main>
        <div className="container">
          {/* Заголовок с ID заявки и статусом */}
          <h1 className="section-title">
            Заявка на технический надзор #{buildRequest.id}
            <span className={`status-badge ${getStatusClass(buildRequest.status)}`}>
              {buildRequest.get_status_display}
            </span>
          </h1>
          
          {buildRequest.is_deleted && (
            <div className="deleted-notice">
              <strong>Внимание!</strong> Эта заявка была удалена. Информация представлена только для просмотра.
            </div>
          )}
          
          {/* Информация о клиенте */}
          <div className="customer-info">
            <h2 className="section-title">Информация о заказчике</h2>
            <form className="customer-form">
              <div className="form-row">
                <div className="form-group">
                  <label>ФИО заказчика*</label>
                  <input
                    type="text"
                    value={buildRequest.user_name}
                    placeholder="Иванов Иван Иванович"
                    readOnly
                  />
                </div>
                <div className="form-group">
                  <label>Телефон*</label>
                  <input
                    type="tel"
                    value={buildRequest.phone}
                    placeholder="+7 (999) 123-45-67"
                    readOnly
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    value={buildRequest.email}
                    placeholder="example@mail.ru"
                    readOnly
                  />
                </div>
                <div className="form-group">
                  <label>Способ оплаты*</label>
                  <input
                    type="text"
                    value={buildRequest.payment_method}
                    placeholder="наличные"
                    readOnly
                  />
                </div>
              </div>
            </form>
          </div>

          {/* Таблица корпусов */}
          <div className="order-table-container">
            <h2 className="section-title">
              Корпусы МГТУ в заявке на технический надзор #{buildRequest.id}
            </h2>
            <table className="order-table">
              <thead>
                <tr>
                  <th>Img</th>
                  <th>Корпус</th>
                  <th>Заключение комиссии</th>
                  <th>Процент готовности</th>
                  <th>Результат</th>
                </tr>
              </thead>
              <tbody>
                {buildRequest.items.map((item, index) => (
                  <tr key={index}>
                    <td>
                      <img
                        src={item.product.image_url}
                        className="product-thumbnail"
                        alt={item.product.title}
                      />
                    </td>
                    <td>{item.product.title}</td>
                    <td>Работы выполнены в соответствии с требованиями</td>
                    <td>100%</td>
                    <td>5.0</td>
                  </tr>
                ))}
                {buildRequest.items.length === 0 && (
                  <tr>
                    <td colSpan="5" style={{ textAlign: 'center' }}>
                      В заявке нет объектов
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}

export default BuildRequestDetail;