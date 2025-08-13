import React, { useState } from 'react';
import { entitiesApi } from '../../entities/api/entityApi';

const initial = {
  legal_name: '',
  registration_number: '',
  tax_id: '',
};

const EntityForm = ({ onCreated }) => {
  const [form, setForm] = useState(initial);
  const [saving, setSaving] = useState(false);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const created = await entitiesApi.create(form);
      onCreated?.(created);
      setForm(initial);
    } catch (err) {
      // noop basic error handling in UI sample
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={onSubmit} className="space-y-3">
      <div>
        <label className="block text-sm">Название</label>
        <input name="legal_name" value={form.legal_name} onChange={onChange} className="border p-2 w-full" />
      </div>
      <div>
        <label className="block text-sm">Рег. номер</label>
        <input name="registration_number" value={form.registration_number} onChange={onChange} className="border p-2 w-full" />
      </div>
      <div>
        <label className="block text-sm">ИНН</label>
        <input name="tax_id" value={form.tax_id} onChange={onChange} className="border p-2 w-full" />
      </div>
      <button type="submit" disabled={saving} className="bg-blue-600 text-white px-4 py-2 rounded">
        {saving ? 'Сохранение...' : 'Создать'}
      </button>
    </form>
  );
};

export default EntityForm;


