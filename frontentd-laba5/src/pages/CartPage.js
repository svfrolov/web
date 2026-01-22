import React from 'react';
import { Link } from 'react-router-dom';

function CartPage() {
  return (
    <div className="container" style={{ padding: '40px 0' }}>
      <Link to="/" style={{ color: '#3498db', textDecoration: 'none', marginBottom: '20px', display: 'block' }}>
        ← Назад к каталогу
      </Link>
      
      <h1 style={{ fontSize: '2rem', marginBottom: '20px', color: '#2c3e50' }}>Корзина заявок</h1>
      <p style={{ color: '#7f8c8d', marginBottom: '30px' }}>
        Здесь отображаются ваши выбранные объекты для строительного контроля
      </p>
      
      <div style={{ 
        backgroundColor: 'white', 
        padding: '30px', 
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '20px', color: '#bdc3c7' }}>📋</div>
        <h3 style={{ color: '#2c3e50', marginBottom: '15px' }}>Корзина пуста</h3>
        <p style={{ color: '#7f8c8d', marginBottom: '25px' }}>
          Добавьте объекты из каталога, чтобы создать заявку на строительный контроль
        </p>
        <Link to="/" className="hero-back-link" style={{ padding: '12px 30px' }}>
          Перейти в каталог
        </Link>
      </div>
    </div>
  );
}

export default CartPage;