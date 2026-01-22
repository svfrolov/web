import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  searchQuery: '',
  category: '',
  sortBy: ''
};

export const filtersSlice = createSlice({
  name: 'filters',
  initialState,
  reducers: {
    setSearchQuery: (state, action) => {
      state.searchQuery = action.payload;
    },
    setCategory: (state, action) => {
      state.category = action.payload;
    },
    setSortBy: (state, action) => {
      state.sortBy = action.payload;
    },
    resetFilters: (state) => {
      state.searchQuery = '';
      state.category = '';
      state.sortBy = '';
    }
  }
});

export const { setSearchQuery, setCategory, setSortBy, resetFilters } = filtersSlice.actions;

export default filtersSlice.reducer;