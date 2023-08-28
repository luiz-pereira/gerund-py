import {snakeCase} from 'lodash';

const BASE_ENDPOINT = 'http://localhost:8000/api/';

export async function get(path) {
  return fetch(
    `${BASE_ENDPOINT + path}`,
    {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    },
  )
    .then((response) => {
      if (!response.ok) {
        throw response;
      }
      return response.json();
    })
    .then((data) => data)
}

export async function post(path, data) {
  const response = await fetch(
    `${BASE_ENDPOINT + path}/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    },
  )
    .then((response) => {
      if (!response.ok) {
        throw response;
      }
      return response.json();
    })
    .then((data) => data)
    .catch((error) => {
      debugger;
    });

  return response;
}

export async function patch(path, id, data) {
  const body = normalizeData(data);
  debugger

  const response = await fetch(
    `${BASE_ENDPOINT + path}/${id}/`,
    {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: body,
    },
  )
    .then((response) => {
      if (!response.ok) {
        throw response;
      }
      return response.json();
    })
    .then((data) => data)
    .catch((error) => {
      return {error: {status: error.status, message: error.statusText}}
    })

  return response;
}

function normalizeData(data) {
  const snakeData =
    Object.entries(data)
      .reduce((acc, [key, val]) => {
        acc[snakeCase(key)] = val
        return acc
      }, {})

  return JSON.stringify(snakeData)
}
