import React from 'react';

const EntityRoles = ({ roles = [] }) => {
  if (!roles.length) return <div>Роли не указаны</div>;
  return (
    <ul className="list-disc pl-6">
      {roles.map((r) => (
        <li key={r.id}>{r.name}</li>
      ))}
    </ul>
  );
};

export default EntityRoles;


