import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { entitiesApi } from '../api/entityApi';

const EntityEdit = () => {
  const { id } = useParams();
  const [form, setForm] = useState(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const res = await entitiesApi.get(id);
        setForm(res);
      } catch (e) {
        setError('Не удалось загрузить сущность');
      }
    })();
  }, [id]);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await entitiesApi.update(id, form);
    } catch (e) {
      setError('Не удалось сохранить изменения');
    } finally {
      setSaving(false);
    }
  };

  if (error) return <div className="text-red-600">{error}</div>;
  if (!form) return <div>Загрузка...</div>;

  return (
    <form onSubmit={onSubmit} className="space-y-3">
      <div>
        <label className="block text-sm">Название</label>
        <input name="legal_name" value={form.legal_name || ''} onChange={onChange} className="border p-2 w-full" />
      </div>
      <div>
        <label className="block text-sm">Рег. номер</label>
        <input name="registration_number" value={form.registration_number || ''} onChange={onChange} className="border p-2 w-full" />
      </div>
      <div>
        <label className="block text-sm">ИНН</label>
        <input name="tax_id" value={form.tax_id || ''} onChange={onChange} className="border p-2 w-full" />
      </div>
      <button type="submit" disabled={saving} className="bg-blue-600 text-white px-4 py-2 rounded">
        {saving ? 'Сохранение...' : 'Сохранить'}
      </button>
    </form>
  );
};

export default EntityEdit;


