import { API_V1 } from '../../../utils/constants';

const base = `${API_V1}/entities`;

export const listEntities = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`${base}/entities/${query ? `?${query}` : ''}`, {
    credentials: 'include',
  });
  if (!res.ok) throw new Error('Failed to fetch entities');
  return res.json();
};

export const getEntity = async (id) => {
  const res = await fetch(`${base}/entities/${id}/`, { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to fetch entity');
  return res.json();
};

export const createEntity = async (data) => {
  const res = await fetch(`${base}/entities/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create entity');
  return res.json();
};

export const updateEntity = async (id, data) => {
  const res = await fetch(`${base}/entities/${id}/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to update entity');
  return res.json();
};

export const entitiesApi = {
  list: listEntities,
  get: getEntity,
  create: createEntity,
  update: updateEntity,
};


