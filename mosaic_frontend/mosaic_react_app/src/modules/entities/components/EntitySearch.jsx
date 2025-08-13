import React, { useState } from 'react';
import { entitiesApi } from '../api/entityApi';

const EntitySearch = ({ onResults }) => {
  const [q, setQ] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    const res = await entitiesApi.list({ search: q });
    onResults?.(res.results || res);
  };

  return (
    <form onSubmit={onSubmit} className="flex gap-2">
      <input value={q} onChange={(e) => setQ(e.target.value)} className="border p-2 flex-1" placeholder="Поиск..." />
      <button className="bg-gray-700 text-white px-3">Найти</button>
    </form>
  );
};

export default EntitySearch;


