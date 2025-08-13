import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { entitiesApi } from '../api/entityApi';
import EntityContacts from '../components/EntityContacts';
import EntityRoles from '../components/EntityRoles';

const EntityDetail = () => {
  const { id } = useParams();
  const [entity, setEntity] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const res = await entitiesApi.get(id);
        setEntity(res);
      } catch (e) {
        setError('Не удалось загрузить сущность');
      }
    })();
  }, [id]);

  if (error) return <div className="text-red-600">{error}</div>;
  if (!entity) return <div>Загрузка...</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">{entity.legal_name}</h1>
      <div>Рег. номер: {entity.registration_number}</div>
      <div>ИНН: {entity.tax_id}</div>
      <EntityRoles roles={entity.roles} />
      <EntityContacts contacts={entity.contacts} />
    </div>
  );
};

export default EntityDetail;


