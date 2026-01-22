import React from 'react';

function DeploymentDiagram() {
  return (
    <div className="deployment-diagram">
      <h2>Диаграмма развертывания</h2>
      <div className="diagram-description">
        <h3>Компоненты системы:</h3>
        <ul>
          <li><strong>Browser</strong> - клиентская часть с React-приложением, Redux Store и Service Worker</li>
          <li><strong>GitHub Pages</strong> - хостинг статических файлов (HTML, CSS, JS, изображения)</li>
          <li><strong>API Server</strong> - бэкенд на Django с REST API, аутентификацией и бизнес-логикой</li>
          <li><strong>Database</strong> - PostgreSQL база данных для хранения информации</li>
        </ul>
        <h3>Протоколы взаимодействия:</h3>
        <ul>
          <li><strong>HTTPS</strong> - для загрузки статических файлов с GitHub Pages</li>
          <li><strong>HTTP/REST</strong> - для взаимодействия между фронтендом и API</li>
          <li><strong>SQL</strong> - для взаимодействия между бэкендом и базой данных</li>
        </ul>
      </div>
    </div>
  );
}

export default DeploymentDiagram;