// Брейкпоинты для адаптивной верстки
export const breakpoints = {
  mobile: '480px',
  tablet: '768px',
  desktop: '1024px'
};

// Медиа-запросы для использования в styled-components или CSS-in-JS
export const media = {
  mobile: `@media (max-width: ${breakpoints.mobile})`,
  tablet: `@media (min-width: ${breakpoints.mobile}) and (max-width: ${breakpoints.tablet})`,
  desktop: `@media (min-width: ${breakpoints.tablet})`,
  notDesktop: `@media (max-width: ${breakpoints.tablet})`
};

export default breakpoints;