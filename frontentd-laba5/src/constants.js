// Константы для приложения
export const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const STATUS_CLASSES = {
  draft: 'status-draft',
  deleted: 'status-deleted',
  submitted: 'status-submitted',
  completed: 'status-completed',
  rejected: 'status-rejected',
  not_found: 'status-not-found'
};

export const STATUS_DISPLAY = {
  draft: 'Черновик',
  deleted: 'Удален',
  submitted: 'Сформирован',
  completed: 'Завершен',
  rejected: 'Отклонен',
  not_found: 'Не найдена'
};