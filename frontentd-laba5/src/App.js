import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import MainPage from './pages/MainPage';
import ServiceDetail from './pages/ServiceDetail';
import RequestPage from './pages/RequestPage';
import BuildRequestDetail from './pages/BuildRequestDetail';
import CartPage from './pages/CartPage';
import './styles/index.css';

function App() {
  const [user, setUser] = useState(null);
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    // Проверяем авторизацию (демо)
    const demoUser = {
      id: 1,
      username: 'demo_user',
      email: 'demo@example.com'
    };
    setUser(demoUser);
    
    // Получаем количество в корзине
    updateCartCount();
    
    // Слушаем изменения в localStorage
    window.addEventListener('storage', updateCartCount);
    
    return () => {
      window.removeEventListener('storage', updateCartCount);
    };
  }, []);

  const updateCartCount = () => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    setCartCount(cart.length);
  };

  return (
    <Router>
      <div className="app">
        <Header user={user} cartCount={cartCount} />
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/service/:id" element={<ServiceDetail />} />
            <Route path="/request" element={<RequestPage />} />
            <Route path="/build-request/:orderId" element={<BuildRequestDetail />} />
            <Route path="/cart" element={<CartPage />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;