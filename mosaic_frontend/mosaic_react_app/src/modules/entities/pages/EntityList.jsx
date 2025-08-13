import React, { useEffect, useState } from 'react';
import { entitiesApi } from '../api/entityApi';

const EntityList = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const res = await entitiesApi.list();
        setData(res.results || res);
      } catch (e) {
        setError('Не удалось загрузить список сущностей');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div className="text-red-600">{error}</div>;

  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">Сущности</h1>
      <table className="min-w-full">
        <thead>
          <tr>
            <th className="text-left p-2">Название</th>
            <th className="text-left p-2">Рег. номер</th>
            <th className="text-left p-2">ИНН</th>
          </tr>
        </thead>
        <tbody>
          {data.map((e) => (
            <tr key={e.id} className="border-t">
              <td className="p-2">{e.legal_name}</td>
              <td className="p-2">{e.registration_number}</td>
              <td className="p-2">{e.tax_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default EntityList;


