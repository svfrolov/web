import { configureStore } from '@reduxjs/toolkit';
import filtersReducer from './slices/filtersSlice';

export const store = configureStore({
  reducer: {
    filters: filtersReducer
  },
  devTools: process.env.NODE_ENV !== 'production'
});

export default store;