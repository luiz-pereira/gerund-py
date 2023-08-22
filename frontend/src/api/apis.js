const BASE_ENDPOINT = 'http://localhost:8000/api/';

export async function get(path) {
  const response = await fetch(
    `${BASE_ENDPOINT + path}/`,
    {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    },
  )
    .then((response) => {
      debugger;
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
      debugger;
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