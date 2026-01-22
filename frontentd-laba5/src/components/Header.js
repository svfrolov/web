import React from "react";
import { Link } from "react-router-dom";
import "../styles/components/header.css";

function Header({ user, cartCount = 0 }) {
  return (
    <>
      {/* Основная шапка */}
      <header>
        <div className="container">
          <div className="home-link">
            <Link to="/">🏠 Домой</Link>
          </div>
          <div className="logo">Строй контроль</div>
          <div className="header-right">
            {user ? <span>{user.username}</span> : null}
          </div>
        </div>
      </header>

      {/* Подхедер с корзиной */}
      <div className="subheader">
        <div className="container">
          <div className="cart-container">
            {user ? (
              <Link to="/request">
                <div className="cart">
                  🛒
                  {cartCount > 0 && (
                    <span className="cart-badge">{cartCount}</span>
                  )}
                </div>
              </Link>
            ) : (
              <div className="cart disabled">
                🛒
                <span className="cart-badge">0</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Секция с заголовком каталога */}
      <section className="catalog-section">
        <div className="container">
          <h1 className="catalog-title">Каталог строительных объектов</h1>
        </div>
      </section>
    </>
  );
}

export default Header;
