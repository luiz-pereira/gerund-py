const BASE_ENDPOINT = 'http://localhost:8000/api/'

export async function get(path) {
    const response = await fetch(BASE_ENDPOINT + path + '/',
        {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
        .then(response => {
          debugger
          if (!response.ok) {
            throw response
          }
          return response.json()
          })
        .then(data => data)
        .catch(error => {
          debugger
        })

      return response
}