import React from 'react';

const EntityContacts = ({ contacts = [] }) => {
  if (!contacts.length) return <div>Контакты не указаны</div>;
  return (
    <ul className="list-disc pl-6">
      {contacts.map((c) => (
        <li key={c.id}>
          {c.first_name} {c.last_name} — {c.email || '—'} {c.phone || ''}
        </li>
      ))}
    </ul>
  );
};

export default EntityContacts;


